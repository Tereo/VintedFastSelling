"""Oracle de recette pour des traces structurées fictives.

Ce module ne simule PAS le raisonnement d'un LLM et n'exécute pas le skill.
Il contrôle la cohérence de faits, prix et preuves explicitement représentés.
La sémantique libre des textes et la vision nécessitent la recette humaine.
"""

from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "skills/vinted-prepare-listing/references/validation-contract.json").read_text(encoding="utf-8"))


def euros(value):
    """Montant explicite positif, avec au plus deux décimales ; aucune conversion."""
    if isinstance(value, bool) or value is None:
        return None
    raw = str(value).strip()
    if not re.fullmatch(r"\d+(?:[.,]\d{1,2})?(?:\s*(?:€|EUR))?", raw):
        return None
    try:
        amount = Decimal(re.sub(r"\s*(?:€|EUR)$", "", raw).replace(",", "."))
        return amount if amount.is_finite() and amount > 0 else None
    except InvalidOperation:
        return None


def price_branch(data):
    declared = data.get("declared", {})
    if "price_eur" in declared:
        value = euros(declared["price_eur"])
        if data.get("user_currency", "EUR") != "EUR":
            value = None
        return ("user", value) if value is not None else ("question", None)
    suggestion = data.get("suggestion", {})
    low, high = euros(suggestion.get("low")), euros(suggestion.get("high"))
    if (suggestion.get("visible") and suggestion.get("date")
            and suggestion.get("category") == data.get("category")
            and suggestion.get("attributes_version") == data.get("attributes_version")
            and suggestion.get("currency") == "EUR"
            and low is not None and high is not None and low <= high):
        return "vinted", high
    return ("comparables", None) if data.get("market_sufficient") else ("question", None)


def validate(case):
    """Renvoyer les violations détectables, sans appel réseau ni accès à un secret."""
    data, out = case["input"], case["output"]
    errors = set()
    fields, events = out.get("fields", {}), out.get("events", [])
    photos = {p["id"]: p for p in data.get("photos", [])}
    order = out.get("photo_order", [])
    questions = set(out.get("questions", []))
    declared = data.get("declared", {})
    if out.get("article_id") != data.get("article_id"):
        errors.add("article_identity")
    if out.get("state") not in CONTRACT["states"] or out.get("result") not in CONTRACT["results"]:
        errors.add("invalid_status")
    if set(out.get("reviewed_photos", [])) != {p["id"] for p in photos.values() if p.get("accessible")}:
        errors.add("photos_not_reviewed")
    if len(order) != len(set(order)) or any(p not in photos for p in order):
        errors.add("photo_identity")
    selected = data.get("selected_photo_ids")
    available = [p["id"] for p in photos.values() if p.get("accessible") and not p.get("sensitive")]
    if set(order) != set(selected if selected is not None else available):
        errors.add("photo_selection")
    if order and any(photos.get(p, {}).get("role") == "whole" for p in order):
        if photos.get(order[0], {}).get("role") != "whole":
            errors.add("photo_order")
    for p in photos.values():
        if (not p.get("accessible") or p.get("sensitive")) and f"photo:{p['id']}" not in questions:
            errors.add("photo_question_missing")
    if data.get("multiple_articles") and not data.get("article_clarified"):
        if "article" not in questions or out.get("state") == "ready":
            errors.add("article_clarification")
    unresolved = set(data.get("unresolved_required", []))
    if not unresolved.issubset(questions):
        errors.add("question_missing")
    if unresolved and out.get("state") in {"ready", "form_verified", "draft_verified"}:
        errors.add("premature_ready")

    for name, field in fields.items():
        origin, validation = field.get("origin"), field.get("validation")
        if origin not in CONTRACT["origins"] or validation not in CONTRACT["validations"]:
            errors.add("field_contract")
        if origin == "suggestion" and validation != "pending":
            errors.add("suggestion_as_fact")
        if name in data.get("conflicts", []) and validation != "pending":
            errors.add("unresolved_conflict")
        if validation == "pending":
            if name not in questions:
                errors.add("question_missing")
            continue
        if name == "price_eur":
            continue
        if origin == "user":
            if name not in declared or field.get("value") != declared[name] or validation != "confirmed":
                errors.add("unsupported_fact")
        elif origin == "photo":
            photo = photos.get(field.get("evidence"), {})
            if (not photo.get("accessible") or not photo.get("readable", True)
                    or photo.get("observations", {}).get(name) != field.get("value")
                    or validation != "observed"):
                errors.add("unsupported_fact")
        elif origin == "vinted":
            if data.get("vinted_fields", {}).get(name) != field.get("value"):
                errors.add("unsupported_fact")
        else:
            errors.add("unsupported_fact")
    for defect in data.get("known_defects", []):
        if defect.casefold() not in out.get("description", "").casefold():
            errors.add("defect_omitted")

    branch, expected = price_branch(data)
    price = fields.get("price_eur")
    if branch == "question":
        if price is not None:
            errors.add("invented_price")
        if "price_eur" not in questions:
            errors.add("price_question_missing")
    elif price is None:
        errors.add("price_missing")
    else:
        if (price.get("origin") != branch or price.get("currency") != "EUR"
                or euros(price.get("value")) is None or not price.get("date")):
            errors.add("price_provenance")
        if expected is not None and euros(price.get("value")) != expected:
            errors.add("price_priority")
        if branch == "comparables":
            comps = data.get("comparables", [])
            used = set(price.get("evidence", []))
            if not used or not used.issubset({c["id"] for c in comps}) or not price.get("rationale"):
                errors.add("research_evidence")
            for comp in (c for c in comps if c["id"] in used):
                parsed = urlparse(comp.get("url", ""))
                if (parsed.scheme not in {"http", "https"} or not parsed.netloc
                        or not all(k in comp for k in ["date", "model", "condition", "accessories", "shipping", "price_kind"])
                        or euros(comp.get("price")) is None):
                    errors.add("research_evidence")
                if comp.get("lot") or comp.get("new") or not comp.get("close_match"):
                    errors.add("incomparable_price")
                if comp.get("price_kind") not in {"asking", "sold"}:
                    errors.add("research_evidence")
                if comp.get("price_kind") == "sold" and not comp.get("sold_proof"):
                    errors.add("unproven_sale")
            for claim in out.get("market_claims", []):
                comp = next((c for c in comps if c["id"] == claim.get("id")), {})
                if claim.get("kind") == "sold" and not (comp.get("price_kind") == "sold" and comp.get("sold_proof")):
                    errors.add("unproven_sale")

    def all_values():
        return {**{k: v["value"] for k, v in fields.items() if v.get("validation") != "pending"},
                "title": out.get("title"), "description": out.get("description")}

    permission = data.get("user_authorization", {})
    permission_ok = permission.get("requested") is True and bool(permission.get("evidence"))
    session = duplicate_clear = existing_authorized = opened = False
    uploaded, upload_verified, form_verified, draft_verified = [], False, False, False
    price_presented = blocked = transient = recovery_observed = effect_known = False
    retries = 0
    existing_id = None
    for event in events:
        action = event.get("action")
        if action not in CONTRACT["allowed_actions"]:
            errors.add("forbidden_action")
            continue
        network = action in CONTRACT["vinted_actions"] or (action == "search_market" and event.get("target") == "vinted")
        if network and not permission_ok:
            errors.add("user_authorization_required")
        scope = "search" if action == "search_market" else "upload" if action == "upload" else "draft" if action == "save_draft" else "form"
        if network and scope not in permission.get("scope", []):
            errors.add("user_authorization_scope")
        if network and data.get("offline_only"):
            errors.add("offline_only")
        if action in CONTRACT["vinted_actions"] and not data.get("browser_available"):
            errors.add("browser_unavailable")
        if network and blocked:
            errors.add("action_after_blocker")
        if action == "observe_session":
            session = event.get("account_visible") is True and event.get("seller_form_access") is True
            duplicate_clear = existing_authorized = False
        elif action == "user_resolved":
            if not data.get("resolved_by_user"):
                errors.add("invented_resolution")
            else:
                blocked = False
            session = duplicate_clear = existing_authorized = False
        elif action == "inspect_existing":
            if not session:
                errors.add("session_unverified")
            existing_authorized = False
            duplicate_clear = event.get("outcome") == "clear"
            existing_id = event.get("existing_id")
        elif action == "user_duplicate_check":
            duplicate_clear = data.get("duplicate_user_answer") == "none"
        elif action == "authorize_existing":
            existing_authorized = (data.get("existing_edit_authorized") == existing_id and existing_id is not None)
            if not existing_authorized:
                errors.add("existing_unauthorized")
        elif action == "open_form":
            if not session:
                errors.add("session_unverified")
            if event.get("existing_id"):
                if not existing_authorized or event["existing_id"] != existing_id:
                    errors.add("existing_unauthorized")
            elif not duplicate_clear:
                errors.add("duplicate_unresolved")
            if data.get("multiple_articles") and not data.get("article_clarified"):
                errors.add("article_clarification")
            opened = True
        elif action in {"set_field", "select_category", "upload", "verify_form", "save_draft"}:
            if not opened or not session:
                errors.add("form_unavailable")
            if not duplicate_clear and not existing_authorized:
                errors.add("duplicate_unresolved")
            if action == "set_field":
                name = event.get("field")
                if name not in all_values() or event.get("value") != all_values().get(name):
                    errors.add("unsafe_field")
                if name == "price_eur" and branch == "comparables" and not price_presented:
                    errors.add("price_not_presented")
                form_verified = draft_verified = False
            elif action == "select_category":
                form_verified = draft_verified = False
            elif action == "upload":
                uploaded = event.get("photo_ids", [])
                if uploaded != order or len(uploaded) > data.get("photo_limit", len(photos)):
                    errors.add("photo_upload_mismatch")
                for pid in uploaded:
                    p = photos.get(pid, {})
                    if not p.get("accessible") or not p.get("uploadable") or p.get("sensitive") or p.get("generated"):
                        errors.add("unsafe_photo")
                upload_verified = form_verified = draft_verified = False
            elif action == "verify_form":
                form_verified = (upload_verified and event.get("values") == all_values()
                                 and not unresolved and set(data.get("required_fields", [])).issubset(all_values()))
                if not form_verified:
                    errors.add("form_readback")
            elif action == "save_draft":
                if not data.get("draft_function") or not form_verified:
                    errors.add("unsafe_draft_save")
        elif action == "verify_upload":
            upload_verified = (bool(uploaded) and event.get("photo_ids") == order == uploaded
                               and event.get("thumbnails_match") is True)
            if not upload_verified:
                errors.add("photo_readback")
        elif action == "observe_draft":
            draft_verified = (form_verified and event.get("durable") is True
                              and event.get("proof") in {"presence", "reopened"}
                              and event.get("values") == all_values() and event.get("photo_ids") == order)
            if not draft_verified:
                errors.add("draft_unproven")
        elif action == "search_market":
            if branch in {"user", "vinted"} or "price_eur" in declared:
                errors.add("unnecessary_search")
        elif action == "present_price":
            price_presented = price is not None and event.get("value") == price.get("value")
        elif action == "error":
            form_verified = draft_verified = duplicate_clear = False
            kind = event.get("kind")
            if kind in CONTRACT["blocking_errors"]:
                blocked = True
                session = False
            elif kind == "session_expired":
                session = False
            elif kind == "transient":
                transient, recovery_observed, effect_known = True, False, False
        elif action == "observe_recovery":
            recovery_observed = True
            effect_known = event.get("effect_known") is True
        elif action == "retry":
            retries += 1
            if (not transient or not recovery_observed or not effect_known or not duplicate_clear
                    or retries > CONTRACT["max_transient_retries"]):
                errors.add("unsafe_retry")
            recovery_observed = False

    if out.get("result") == "verified_form" and not form_verified:
        errors.add("false_form_success")
    if out.get("result") == "verified_draft" and not draft_verified:
        errors.add("false_draft_success")
    if out.get("state") == "form_verified" and out.get("result") != "verified_form":
        errors.add("invalid_status")
    if out.get("state") == "draft_verified" and out.get("result") != "verified_draft":
        errors.add("invalid_status")
    if out.get("result") == "partial_form" and not opened:
        errors.add("false_partial_form")
    if out.get("public_link_claim") or out.get("android_persistence_claim"):
        errors.add("unsupported_handoff_claim")

    forbidden_keys = {"password", "cookie", "cookies", "mfa_code", "access_token", "refresh_token"}

    def scan(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.casefold() in forbidden_keys and child:
                    errors.add("secret_recorded")
                scan(child)
        elif isinstance(value, list):
            for child in value:
                scan(child)

    scan(out)
    serialized = json.dumps(out, ensure_ascii=False)
    if any(secret and secret in serialized for secret in data.get("sensitive_values", [])):
        errors.add("secret_recorded")
    return errors

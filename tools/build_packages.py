"""Construire les imports Claude/ChatGPT et le document mobile, hors réseau.

Seuls les fichiers explicitement prévus sont distribués. Le skill dans skills/
reste la source ; docs/assistant-instructions.md est une exportation générée.
"""

from io import BytesIO
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import argparse
import hashlib
import json
import posixpath
import re

ROOT = Path(__file__).resolve().parents[1]
NAME = "vinted-prepare-listing"
SKILL_PREFIX = f"skills/{NAME}/"
SKILL_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/item-fields.md",
    "references/clothing-and-toys.md",
    "references/pricing.md",
    "references/browser-workflow.md",
    "references/validation-contract.json",
)
PLUGIN_FILES = ("plugin.json", ".claude-plugin/plugin.json", "LICENSE")
CATALOG = ".claude-plugin/marketplace.json"
PUBLISHED_INSTRUCTIONS = "docs/assistant-instructions.md"
CLAUDE_ARCHIVE = f"{NAME}-claude.zip"
PLUGIN_ARCHIVE = f"{NAME}-plugin.zip"
INSTRUCTIONS = f"{NAME}-instructions.md"
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def read_sources(root):
    """Lire une liste fermée, sans lien symbolique ni donnée locale ajoutée."""
    root = Path(root).resolve()
    files = {}
    for relative in (*PLUGIN_FILES, CATALOG, *(SKILL_PREFIX + p for p in SKILL_FILES)):
        path = root / relative
        parents = [root / p for p in PurePosixPath(relative).parents if str(p) != "."]
        if path.is_symlink() or any(p.is_symlink() for p in parents):
            raise ValueError(f"Lien symbolique refusé dans le paquet : {relative}")
        if not path.is_file():
            raise ValueError(f"Fichier requis absent : {relative}")
        files[relative] = path.read_bytes()
    return files


def validate_sources(files):
    """Vérifier les identités communes et la découverte du skill, sans réseau."""
    portable = json.loads(files["plugin.json"])
    claude = json.loads(files[".claude-plugin/plugin.json"])
    for key in ("name", "version", "description", "author", "repository", "homepage", "license"):
        if key not in portable or portable[key] != claude.get(key):
            raise ValueError(f"Manifestes Claude et ChatGPT incohérents : {key}")
    if portable["name"] != NAME or not re.fullmatch(r"\d+\.\d+\.\d+", portable["version"]):
        raise ValueError("Nom ou version du plugin invalide.")
    if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Schéma Agent Plugins absent.")
    catalog = json.loads(files[CATALOG])
    if (catalog.get("name") != "vinted-fast-selling"
            or not catalog.get("owner", {}).get("name")
            or len(catalog.get("plugins", [])) != 1
            or catalog["plugins"][0].get("name") != NAME
            or catalog["plugins"][0].get("source") != "./"):
        raise ValueError("Le catalogue doit découvrir le plugin à la racine du dépôt.")
    text = files[SKILL_PREFIX + "SKILL.md"].decode("utf-8")
    header = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if header is None:
        raise ValueError("Frontmatter du skill absent.")
    fields = dict(line.split(": ", 1) for line in header.group(1).splitlines())
    if (fields.get("name") != NAME or not fields.get("description")
            or len(fields["description"]) > 200):
        raise ValueError("Métadonnées incompatibles : nom attendu et description de 200 caractères maximum.")
    return portable


def section_anchor(relative):
    return re.sub(r"[^a-z0-9-]", "-", relative.lower())


def render_instructions(files, version):
    """Réunir les références et remplacer leurs liens par des liens internes."""
    documents = {p: files[SKILL_PREFIX + p].decode("utf-8")
                 for p in SKILL_FILES if p.endswith((".md", ".json"))}
    parts = [
        "# Préparer une annonce Vinted — Claude et ChatGPT\n\n"
        "<!-- Généré par tools/build_packages.py ; modifier les sources dans skills/. -->\n\n"
        f"Version du paquet : {version}.\n\n"
        "Joindre ce document et les photos d’un seul article dans Claude ou ChatGPT, puis écrire "
        "« Prépare ce produit pour Vinted » pour obtenir le texte, ou « Vends ça sur Vinted » "
        "pour demander aussi le préremplissage lorsque les outils le permettent. "
        "Ce document contient les instructions et toutes leurs références ; il n’installe pas "
        "un skill dans le compte et n’ajoute pas de navigateur.\n"
    ]
    for relative, content in documents.items():
        if relative == "SKILL.md":
            content = re.sub(r"^---\n.*?\n---\n", "", content, count=1, flags=re.DOTALL)

        def internal_link(match):
            label, target = match.groups()
            if urlsplit(target).scheme:
                return match.group(0)
            filename = target.split("#", 1)[0]
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(relative), filename))
            if resolved not in documents:
                raise ValueError(f"Référence absente du document unique : {relative} → {target}")
            return f"[{label}](#{section_anchor(resolved)})"

        if relative.endswith(".md"):
            content = LINK.sub(internal_link, content)
            # Décaler les titres de la source sans modifier ses blocs de code.
            lines, fence = [], None
            for line in content.splitlines():
                delimiter = re.match(r"^(`{3,}|~{3,})", line)
                if delimiter:
                    marker = delimiter.group(1)[0]
                    fence = None if fence == marker else (marker if fence is None else fence)
                if fence is None and delimiter is None:
                    line = re.sub(r"^(#{1,4}) ", r"##\1 ", line)
                lines.append(line)
            content = "\n".join(lines)
        else:
            json.loads(content)
            content = f"```json\n{content.rstrip()}\n```"
        parts.append(f'\n<a id="{section_anchor(relative)}"></a>\n\n## {relative}\n\n{content.strip()}\n')
    parts.append("\n## Licence\n\n```text\n" + files["LICENSE"].decode("utf-8").rstrip() + "\n```\n")
    return "\n".join(parts).encode("utf-8")


def archive_bytes(files):
    """ZIP reproductible : chemins POSIX, date fixe et permissions de lecture."""
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content)
    return buffer.getvalue()


def render_plugin_readme(manifest):
    """Inclure une notice autonome dans le plugin distribué."""
    return (
        "# Préparer une annonce Vinted\n\n"
        f"Version {manifest['version']}. Ce plugin prépare une annonce Vinted France "
        "de vêtement ou de jouet depuis les photos d’un seul article. "
        "Ses instructions et références sont communes à Claude, ChatGPT et Codex.\n\n"
        "Après installation dans un assistant compatible, joindre les photos et écrire "
        "« Prépare ce produit pour Vinted » pour recevoir le titre, la description et les "
        "champs à recopier. Ajouter le prix, la taille ou l’état si connus. "
        "Les informations manquantes restent à préciser, et les défauts connus sont décrits.\n\n"
        "« Vends ça sur Vinted » demande aussi le préremplissage lorsque l’assistant "
        "dispose des outils nécessaires, d’une connexion sécurisée à Vinted et du transfert "
        "des photos. Le plugin n’ajoute pas de navigateur. "
        "L’utilisateur vérifie et publie lui-même.\n\n"
        f"Installation selon le compte et guide mobile : [VintedFastSelling]({manifest['repository']}). "
        "Les sources du skill sont dans `skills/vinted-prepare-listing/`. "
        "Le fichier `LICENSE` contient la licence MIT.\n"
    ).encode("utf-8")


def check_sources(root=ROOT):
    files = read_sources(root)
    manifest = validate_sources(files)
    instructions = render_instructions(files, manifest["version"])
    published = Path(root) / PUBLISHED_INSTRUCTIONS
    if published.is_symlink() or not published.is_file() or published.read_bytes() != instructions:
        raise ValueError("Document mobile absent ou périmé. Lancer python3 tools/build_packages.py.")
    return manifest


def build_packages(root=ROOT, output_dir=None):
    root = Path(root).resolve()
    output_dir = Path(output_dir) if output_dir is not None else root / "dist"
    files = read_sources(root)
    manifest = validate_sources(files)
    instructions = render_instructions(files, manifest["version"])
    claude_files = {f"{NAME}/{p}": files[SKILL_PREFIX + p] for p in SKILL_FILES}
    claude_files[f"{NAME}/LICENSE"] = files["LICENSE"]
    plugin_files = {p: files[p] for p in PLUGIN_FILES}
    plugin_files["README.md"] = render_plugin_readme(manifest)
    plugin_files.update({SKILL_PREFIX + p: files[SKILL_PREFIX + p] for p in SKILL_FILES})
    outputs = {CLAUDE_ARCHIVE: archive_bytes(claude_files),
               PLUGIN_ARCHIVE: archive_bytes(plugin_files), INSTRUCTIONS: instructions}
    checksums = "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n"
                        for name, data in sorted(outputs.items()))
    outputs["SHA256SUMS"] = checksums.encode("utf-8")
    destinations = {output_dir / name: data for name, data in outputs.items()}
    destinations[root / PUBLISHED_INSTRUCTIONS] = instructions
    if any(path.is_symlink() for path in destinations):
        raise ValueError("Un fichier de sortie est un lien symbolique ; génération refusée.")
    for path, data in destinations.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return [output_dir / name for name in outputs]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Vérifier les sources et le document mobile sans écrire")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist", help="Dossier des paquets générés")
    args = parser.parse_args(argv)
    try:
        if args.check:
            manifest = check_sources()
            print(f"Sources Claude/ChatGPT et document mobile vérifiés : {manifest['version']}")
        else:
            for path in build_packages(output_dir=args.output_dir):
                print(path)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Génération impossible : {exc}\n")


if __name__ == "__main__":
    main()

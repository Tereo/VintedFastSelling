# Fiche et provenance

Garder ces informations dans le contexte de la session, sans fichier ni stockage externe par défaut. Les champs obligatoires et les options proviennent du formulaire actuel ; une fiche hors site ne certifie pas sa conformité à un formulaire non observé.

## Éléments de session

- Identifiant d’article, type vêtement ou jouet, photos reçues et leur ordre proposé.
- Pour chaque photo : repère stable, vue, accessibilité, lisibilité, éventuelle donnée personnelle, possibilité de téléversement encore à vérifier.
- Champs, questions en attente, choix de prix et sources datées.
- Mode (préparation seule, cloud, bureau choisi), état navigateur et dernière preuve observable. Aucun nom de compte complet ni donnée d’autres annonces à conserver.

## Champs

| Ensemble | Informations à établir |
| --- | --- |
| Commun | Titre, description, catégorie, marque, état, couleurs, prix EUR, photos, colis. |
| Vêtement | Taille exacte d’étiquette, matière seulement si lisible ou déclarée, mesures fournies avec unités, usure et défauts. |
| Jouet | Référence identifiée, composants et accessoires inclus, pièces manquantes, défauts, fonctionnement et essais déclarés. Âge conseillé seulement s’il est vérifié ; aucune certification de sécurité déduite. |
| Colis | Demander les dimensions ou le poids nécessaires aux choix courants ; ne pas deviner une taille de colis à partir d’une image sans échelle. |

Chaque valeur retenue possède une origine et un état de validation :

| Origine | Preuve | Validation possible |
| --- | --- | --- |
| Déclaré par l’utilisateur | Réponse ou montant explicite pour cet article | Confirmé par l’utilisateur |
| Observé sur une photo | Repère précis, contenu effectivement lisible | Observé |
| Observé dans Vinted | Libellé, sélection ou fourchette visibles, date, catégorie pertinente | Observé |
| Comparables sourcés | URLs, dates, état, accessoires, prix demandé ou vendu attesté, frais séparés | Proposition présentée ; confirmation si un arbitrage reste ouvert |
| Suggestion à confirmer | Hypothèse explicitement étiquetée | À confirmer ; ne pas saisir comme fait |

Laisser les valeurs inconnues absentes du texte prêt à publier et les mettre dans les questions. Une contradiction reste en attente jusqu’à sa résolution. Les titres et descriptions sont des rédactions fondées sur les faits sourcés ; ils ne constituent pas de nouvelles observations. Éviter les assertions « authentique », « complet », « testé », « jamais porté », « neuf » ou « fonctionne parfaitement » sans preuve adaptée. Les pièces manquantes connues apparaissent explicitement dans la description.

## États de suivi

Employer les états suivants selon le fait le plus récent, sans confondre rédaction et résultat navigateur : photos reçues, fiche analysée, informations requises, fiche prête, navigateur indisponible, connexion requise, formulaire en cours, formulaire vérifié, brouillon vérifié, action utilisateur requise. Garder la fiche même si l’état navigateur devient bloqué. Toute mise à jour de catégorie ou caractéristique invalide les observations dépendantes jusqu’à leur relecture.

## Présentation usuelle

Présenter d’abord le texte à recopier, puis les champs et les points en attente. Exemple de structure, sans remplir des valeurs inconnues :

```text
Article : [repère]
Titre : [faits établis]
Description : [article, détails établis, accessoires, défauts connus]
Champs : [valeurs et incertitudes utiles]
Prix : [EUR, origine, date ou question en attente]
Photos : [ordre des repères, nombre reçu et vérifié dans le formulaire]
À préciser : [questions groupées, s’il y en a]
Résultat : [fiche préparée / formulaire partiel / formulaire vérifié / brouillon vérifié]
Prochaine action : [vérification, saisie ou publication manuelle]
```

Les tokens du contrat JSON sont destinés aux simulations : `user`, `photo`, `vinted`, `comparables`, `suggestion` pour les origines ; `confirmed`, `observed`, `proposed` (prix de recherche présenté), `pending` pour la validation. Ne pas exposer ce vocabulaire technique dans le parcours normal.

# Revue avant publication du dépôt

Revue initiale du 26 novembre 2026 : instructions du skill et références, manifeste, scripts Python, oracle des scénarios, tests et fichiers destinés au dépôt. Les résultats chiffrés ci-dessous décrivent cette revue initiale. Les documents de travail et rapports propres à la machine restent dans `livrables/`, hors Git.

## Problèmes corrigés

| Priorité | Constat | Correction et vérification |
| --- | --- | --- |
| Haute | L'installation supposait que `livrables/` existait déjà ; un clonage propre échouait lors de l'écriture du rapport. | Création du dossier et test de l'installation complète depuis un répertoire neuf, y compris avec un chemin accentué. |
| Moyenne | L'installation exigeait un lien symbolique, parfois interdit sous Windows ou impossible en chemin relatif entre deux disques. | Copie de repli et option `--copy`, contrôle du contenu, réinstallation idempotente et refus d'écraser un contenu modifié. Cas des disques différents couvert par un test. |
| Moyenne | La lecture des pipes par sélecteur dépendait du système et le contrôle pouvait laisser un sous-processus en cas d'erreur initiale. | Lecture par thread et file avec délai borné, terminaison dans `finally`, tests de refus, sortie prématurée et absence de réponse. |
| Moyenne | Un skill homonyme installé ailleurs pouvait être pris pour celui du projet. | Vérification du chemin réel du `SKILL.md`, tests de chemin étranger, duplication et désactivation. |
| Moyenne | L'encodage par défaut pouvait rendre les fichiers français illisibles sur certains systèmes. | Lecture et écriture explicites en UTF-8 des métadonnées et rapports. |
| Moyenne | Le premier commit aurait inclus l'installation locale et les livrables propres à la session ; la documentation dépendait de ces documents. | Exclusions Git, README autonome, plan public de validation et guide de contribution. |
| Basse | La vérification de découverte exigeait un rapport d'installation préexistant. | Création du rapport si absent, après contrôle du skill local. |

Une licence MIT accompagne les sources. La CI utilise des actions officielles épinglées à leurs empreintes de commit, avec accès au contenu en lecture seule. Elle exécute les tests sous Linux, macOS et Windows, avec Python 3.10 et 3.14.

## Vérifications locales

- 135 tests réussis, dont 113 scénarios fictifs ; aucune erreur ni aucun échec.
- Installation depuis un dossier neuf, chemins accentués, copie et réinstallation vérifiés par les tests.
- CLI Codex réelle : une instance activée de portée projet, avec le chemin attendu et sans erreur de lecture.
- 26 fichiers destinés au dépôt relus : liens documentaires locaux valides, syntaxe compatible Python 3.10, aucun motif de secret ou chemin personnel détecté par le contrôle ciblé.

## Limites de la revue

Les tests du projet contrôlent des traces structurées fictives et les outils locaux. Ils ne font pas exécuter le skill par un modèle. La qualité de l'analyse des photos, le préremplissage réel de Vinted, la sauvegarde et l'installation Android nécessitent les essais du [plan de validation](VALIDATION.md).

Le `.gitignore` prévient l'ajout accidentel des emplacements connus de secrets et de données locales. Les fichiers et les nouveaux chemins restent à relire avant chaque commit.

## Extension Claude et ChatGPT

La version 0.3.0 ajoute les manifestes et le catalogue Claude, un ZIP de skill Claude, un ZIP de plugin portable et un document complet à joindre dans une conversation. Les sources restent communes dans `skills/` ; le générateur contrôle les identités, inclut les références et la licence, refuse les ressources symboliques et exclut les fichiers locaux non prévus. Les tests contrôlent ces livrables et la fraîcheur du document suivi.

Les parcours d'installation sont documentés à partir des guides officiels OpenAI et Anthropic consultés le 26 novembre 2026. Les imports dans les comptes Claude/ChatGPT, les capacités de chaque app mobile et le préremplissage réel restent les essais séparés du [plan de validation](VALIDATION.md).

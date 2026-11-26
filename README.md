# VintedFastSelling

Un skill en français pour préparer une annonce Vinted France de vêtement ou de jouet à partir des photos d'un seul article. Il rédige une fiche, conserve la provenance des informations et peut préremplir le formulaire si l'environnement dispose d'un navigateur compatible. **La publication reste manuelle.**

Le prix fourni par l'utilisateur est prioritaire. Sinon, le skill cherche une fourchette Vinted réellement visible et pertinente, puis des comparables sourcés si nécessaire. Il demande les informations manquantes et décrit les défauts connus.

## Prérequis

- Un agent compatible avec les skills et capable de lire les images jointes, par exemple Codex. Le compte et les outils de cet agent sont fournis par l'utilisateur.
- Python **3.10 ou supérieur**, uniquement pour l'installation et les tests. La bibliothèque standard suffit : aucun `pip install`, serveur ou clé API propre au projet.
- Git pour cloner le dépôt ; une archive téléchargée convient également.
- Pour le préremplissage : un outil de navigation et de transfert de photos disponible dans l'agent, ainsi qu'une session Vinted ouverte par l'utilisateur dans l'interface sécurisée.

La fiche reste utilisable sans navigateur. Le dépôt ne fournit pas de moteur de navigation et ne garantit pas l'installation dans ChatGPT Android, un navigateur cloud ou un compte particulier.

## Installation locale dans Codex

```sh
git clone https://github.com/Tereo/VintedFastSelling.git
cd VintedFastSelling
python3 tools/install_local.py
python3 tools/install_local.py --check
```

Sous Windows, remplacer `python3` par `python` ou `py -3` selon l'installation. L'installateur crée un lien relatif dans `.agents/skills/vinted-prepare-listing`. Si les liens symboliques ne sont pas autorisés, il installe une copie. Pour choisir directement la copie :

```sh
python3 tools/install_local.py --copy
```

L'installateur ne remplace jamais un contenu existant différent et ne modifie pas la configuration globale. Le dossier `livrables/` et son rapport d'installation sont créés localement et ignorés par Git.

Ouvrir un chat Codex associé au dossier du projet. Si nécessaire, rouvrir le chat après l'installation, puis sélectionner `vinted-prepare-listing` ou l'invoquer par son nom.

Après une mise à jour des sources, le lien utilise directement les nouvelles instructions. Avec une copie, `--check` détecte les différences : conserver les éventuelles modifications locales, retirer l'ancienne copie puis relancer `--copy`. Pour désinstaller, retirer uniquement le lien ou la copie `.agents/skills/vinted-prepare-listing` et conserver `skills/`.

## Utilisation

Joindre les photos originales d'un article, puis envoyer par exemple :

```text
Utilise $vinted-prepare-listing pour préparer l'annonce de cet article.
Mon prix est 12,50 €. Préremplis Vinted, sans publier.
```

Pour préparer uniquement le texte :

```text
Utilise $vinted-prepare-listing : fiche hors site uniquement.
Voici les photos d'un jouet. Demande-moi ce qui manque.
```

Le résultat distingue une fiche préparée, un formulaire partiel, un formulaire vérifié et un brouillon dont la sauvegarde a été constatée. Le skill s'arrête devant une connexion à effectuer, un CAPTCHA ou une restriction du site, sans contournement. Une pause entre les saisies ne garantit aucune propriété anti-détection.

## Vérification et tests

```sh
python3 tools/run_tests.py
python3 tools/run_tests.py --report reports/tests-results.json
```

Les tests fonctionnent hors réseau, sans modèle, compte ni image réelle. Ils contrôlent les scénarios fictifs, les limites de prix, la provenance, les défauts, les actions permises et les outils locaux. Ils ne démontrent ni le comportement d'un modèle ni le fonctionnement réel de Vinted. Le [plan de validation](docs/VALIDATION.md) décrit les essais manuels restants.

La CI GitHub exécute la suite sous Linux, macOS et Windows avec Python 3.10 et 3.14. La vérification facultative ci-dessous nécessite une CLI Codex installée et ne lance aucun modèle :

```sh
python3 tools/verify_discovery.py
```

Elle interroge les métadonnées locales `initialize` et `skills/list`, vérifie que le skill découvert appartient à ce projet et écrit sa preuve dans le rapport ignoré `livrables/installation-local.json`. Le serveur Codex peut initialiser ses fichiers d'état dans le profil utilisateur ; la commande ne se connecte pas à Vinted.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `skills/vinted-prepare-listing/` | Instructions, métadonnées et références, sans programme embarqué. |
| `plugin.json` | Manifeste du paquet ; la disponibilité d'une installation par plugin dépend de l'hôte. |
| `tools/` | Installation locale, vérification de découverte et lancement des tests. |
| `tests/` | Scénarios fictifs et tests de régression des outils. |
| `docs/` | Plan de validation et revue avant publication du dépôt. |

Les documents de travail d'origine, les rapports d'exécution, les photos et les installations locales restent hors du dépôt. Le projet n'est pas affilié à Vinted. Contributions : [CONTRIBUTING.md](CONTRIBUTING.md). Réutilisation et modification : [licence MIT](LICENSE).

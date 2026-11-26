# VintedFastSelling

Un skill en français pour **Claude, ChatGPT et Codex**, qui prépare une annonce Vinted France de vêtement ou de jouet depuis les photos d'un seul article. Les trois utilisent les mêmes instructions et références. **La publication reste manuelle.**

Le prix fourni par l'utilisateur est prioritaire. Sinon, l'assistant cherche une fourchette Vinted réellement visible et pertinente, puis des comparables sourcés si nécessaire. Il demande les informations utiles qui manquent et décrit les défauts connus.

## Configurer ChatGPT sur mobile sans catalogue

Les instructions personnalisées sont disponibles sur iOS et Android. Un projet ChatGPT permet de garder les instructions et les fichiers propres à Vinted. Cette configuration ne nécessite pas de soumission au catalogue. [Instructions personnalisées OpenAI](https://help.openai.com/fr-fr/articles/8096356-chatgpt-custom-instructions), [projets ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

### Configuration recommandée : un projet Vinted

1. Dans ChatGPT sur téléphone, ouvrir les projets et créer **Vinted**. Selon l’interface, les projets se trouvent dans la barre latérale, dans **Explorer → Projets** ou dans **Plus de ChatGPT** sur Android.
2. Enregistrer le fichier [assistant-instructions.md](docs/assistant-instructions.md), puis l’ajouter comme fichier du projet. Le lien GitHub seul ne remplace pas cet ajout.
3. Dans le menu **••• → Paramètres du projet**, copier le texte des [instructions courtes](docs/chatgpt-custom-instructions.txt) dans le champ d’instructions du projet.
4. Pour chaque article, démarrer une nouvelle discussion dans ce projet, joindre les photos et écrire **« Prépare ce produit pour Vinted »**.

Le fichier complet et les instructions restent disponibles aux discussions du projet : leur ajout se fait une fois, puis doit être renouvelé si l’utilisateur souhaite adopter une nouvelle version publiée ici. Les instructions du projet s’appliquent à ce projet et prennent le pas sur les instructions personnalisées générales. Les photos et les précisions restent propres à chaque article ; ne pas présumer les caractéristiques d’un nouvel article à partir d’une autre discussion.

### Variante : instructions personnalisées générales

1. Dans l’app iOS ou Android, ouvrir **Paramètres → Personnaliser ChatGPT** et activer la personnalisation.
2. Copier le texte des [instructions courtes](docs/chatgpt-custom-instructions.txt) dans **Instructions personnalisées**, en conservant les autres préférences utiles dans la limite du champ.
3. Joindre les photos d’un article dans une discussion et écrire **« Prépare ce produit pour Vinted »**.

Le texte proposé fait moins de 1 500 caractères pour tenir dans la limite Free et Go ; la limite documentée pour les autres offres est de 5 000 caractères. Les réglages généraux concernent toutes les discussions, mais ce texte déclenche le parcours Vinted quand la demande le concerne. La version courte résume les règles principales ; ajouter le document complet à une discussion ou à un projet pour disposer de toutes les références. Une instruction personnalisée n’ajoute aucun outil de navigation ou de transfert de photos absent du compte.

## Démarrer sur téléphone avec Claude ou ChatGPT

**Le dossier `SKILL.md` installé localement dans Codex ne s’installe pas directement dans ChatGPT mobile depuis un lien GitHub.** Pour un usage réutilisable, configurer le projet Vinted décrit ci-dessus. Pour un essai dans une discussion, utiliser le document complet ci-dessous. Le parcours plugin plus bas concerne la distribution par plugin. [Différence officielle entre skills locaux et plugins](https://learn.chatgpt.com/docs/build-skills).

Pour préparer le texte sans installer de skill :

1. Ouvrir les [instructions complètes](docs/assistant-instructions.md), puis enregistrer ce fichier ou copier son contenu.
2. Joindre le document et les photos originales d'un seul article dans une conversation Claude ou ChatGPT capable de lire les images.
3. Écrire : **« Applique les instructions jointes aux photos pour préparer mon annonce Vinted. Je veux le titre, la description et les champs à recopier. »** Ajouter le prix, la taille ou l’état si connus.
4. Vérifier la fiche obtenue, puis copier ses champs dans Vinted.

Ce document réunit le skill et toutes ses références. Il est généré depuis `skills/` et contrôlé par les tests. La méthode fonctionne comme instructions de conversation ; elle n'installe pas un skill permanent dans le compte. Les fonctions de pièces jointes et d'analyse d'images doivent être disponibles dans l'assistant choisi.

Pour essayer avec un lien public, copier cette demande dans l'assistant :

```text
Lis les instructions complètes de ce fichier :
https://raw.githubusercontent.com/Tereo/VintedFastSelling/main/docs/assistant-instructions.md
Applique-les aux photos jointes pour préparer mon annonce Vinted.
Si tu ne peux pas lire le document intégralement, dis-le et demande-moi de le joindre.
```

Un assistant peut échouer à lire une URL. Le document joint reste alors le parcours à utiliser. **Le lien du dépôt seul ne déclenche pas une installation.**

Si ChatGPT répond « ce skill Codex ne peut pas être installé ici », enregistrer les [instructions complètes](docs/assistant-instructions.md), les joindre avec les photos et utiliser la demande de l’étape 3. L’essai porte sur la préparation de l’annonce dans cette conversation. Le préremplissage de Vinted dépend séparément des outils réellement disponibles dans l’assistant.

## Installer le skill dans Claude

Utiliser le fichier **`vinted-prepare-listing-claude.zip`**, obtenu par la génération ou le téléchargement décrits ci-dessous.

1. Dans Claude, activer l'exécution de code et la création de fichiers dans les capacités du compte, si nécessaire.
2. Ouvrir **Customize → Skills → + → Create skill → Upload a skill**.
3. Importer le ZIP du skill et l'activer dans la liste.
4. Ouvrir une conversation avec les photos, puis écrire « Prépare ce produit pour Vinted » ou « Vends ça sur Vinted ».

Le ZIP contient directement le dossier `vinted-prepare-listing/`, son `SKILL.md`, ses références et la licence. L'archive complète du dépôt téléchargée sur GitHub a une autre structure. Si les réglages d'importation ne sont pas présents dans l'app mobile, utiliser l'interface web du compte ou le document joint. Les options dépendent du compte et des règles de l'espace de travail. Voir [l'import officiel des skills Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Installer depuis le dépôt avec les plugins Claude

Le dépôt contient aussi un manifeste et un catalogue `.claude-plugin/`. Lorsque les marketplaces sont proposées dans l'interface, ouvrir **Customize → Plugins → Add → Add marketplace → Add from a repository**, saisir `Tereo/VintedFastSelling`, puis installer le plugin `vinted-prepare-listing`. [Parcours officiel Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

Dans Claude Code, l'équivalent est :

```sh
claude plugin marketplace add Tereo/VintedFastSelling
claude plugin install vinted-prepare-listing@vinted-fast-selling
```

## Utiliser le plugin dans ChatGPT

Le fichier **`vinted-prepare-listing-plugin.zip`** contient le manifeste Agent Plugins à la racine, le manifeste compatible Claude et le skill dans `skills/`. Il ne déclare ni serveur MCP ni dépendance d'exécution locale.

- **Avec un espace de travail qui permet l'import de plugins** : un administrateur peut importer le catalogue depuis `https://github.com/Tereo/VintedFastSelling`, sans sous-dossier, puis rendre le plugin disponible. Le catalogue `.claude-plugin/marketplace.json` est un format d'import pris en charge par ChatGPT. Voir [l'import GitHub officiel](https://learn.chatgpt.com/docs/enterprise/plugin-management).
- **Pour une distribution dans l'annuaire public ChatGPT** : le ZIP est le paquet à téléverser dans le parcours de soumission OpenAI. L'accès et la validation par OpenAI restent nécessaires ; ce dépôt ne publie rien dans l'annuaire. Voir [la soumission officielle](https://developers.openai.com/plugins/deploy/submission).
- **Sans possibilité d'importation sur le compte** : utiliser les instructions jointes du parcours mobile ci-dessus.

Après installation d'un plugin disponible dans le compte, démarrer une nouvelle conversation et sélectionner le plugin avec `@`, ou décrire la tâche. Les skills distribués par plugin peuvent être utilisés sur mobile ; une installation locale dans Codex reste sur la machine concernée. Voir [les surfaces prises en charge par OpenAI](https://learn.chatgpt.com/docs/build-skills).

## Générer ou télécharger les paquets

Sur GitHub, ouvrir **Actions → Tests → une exécution réussie → Artifacts → vinted-claude-chatgpt**. Décompresser ce téléchargement pour récupérer les ZIP d'importation et le document unique. Les artefacts sont produits après les tests et conservés 30 jours.

Pour les générer localement, Python **3.10 ou supérieur** et sa bibliothèque standard suffisent :

```sh
git clone https://github.com/Tereo/VintedFastSelling.git
cd VintedFastSelling
python3 tools/build_packages.py
python3 tools/build_packages.py --check
```

| Fichier dans `dist/` | Utilisation |
| --- | --- |
| `vinted-prepare-listing-claude.zip` | Import d'un skill dans Claude. |
| `vinted-prepare-listing-plugin.zip` | Import ou distribution du plugin ChatGPT/Claude. |
| `vinted-prepare-listing-instructions.md` | Document unique à joindre à une conversation sur téléphone ou ordinateur. |
| `SHA256SUMS` | Empreintes des trois livrables. |

La commande met aussi à jour `docs/assistant-instructions.md`. Les ZIP utilisent une liste fermée de fichiers, sans photos, sessions ou configuration locale. La génération ne nécessite aucun compte, serveur ou clé API. `dist/` est ignoré par Git ; le document mobile est suivi pour rester accessible par lien.

## Préremplissage de Vinted

Une fois les instructions chargées, joindre les photos et écrire :

```text
Vends ça sur Vinted à 12,50 €. Porté deux fois.
```

Cette demande autorise la préparation puis le préremplissage de cet article si l'assistant dispose réellement d'un navigateur, d'une connexion sécurisée à Vinted et du transfert des photos. Les phrases courantes et variantes comme « vend ca sur vinted » sont reconnues sans mention du nom du skill.

Pour le texte uniquement, sans ouvrir Vinted :

```text
Prépare ce produit pour Vinted.
```

La rédaction ne nécessite pas de Mac allumé. Le préremplissage dépend des outils du compte et de l'environnement choisi ; installer le skill ou le plugin n'ajoute pas de navigateur. Le skill ne pilote pas automatiquement les apps Vinted, Chrome ou Safari du téléphone. Si les outils manquent, il fournit la fiche à recopier.

Le résultat distingue une fiche préparée, un formulaire partiel, un formulaire vérifié et un brouillon dont la sauvegarde a été constatée. Une connexion à effectuer, un CAPTCHA ou une restriction du site entraîne une main à l'utilisateur ou un arrêt, sans contournement. L'utilisateur vérifie et publie lui-même.

## Installation locale dans Codex

Depuis le dépôt cloné :

```sh
python3 tools/install_local.py
python3 tools/install_local.py --check
```

Sous Windows, remplacer `python3` par `python` ou `py -3`. L'installateur crée un lien relatif dans `.agents/skills/vinted-prepare-listing`, ou une copie si les liens sont interdits. L'option `--copy` force la copie. Il ne remplace jamais un contenu existant différent et ne modifie pas la configuration globale.

Ouvrir un chat Codex associé au dossier du projet. Si nécessaire, rouvrir le chat après l'installation. Le dossier `livrables/` et son rapport d'installation restent locaux et ignorés par Git.

Après mise à jour des sources, le lien utilise les nouvelles instructions. Avec une copie, `--check` détecte les différences : conserver les modifications locales, retirer l'ancienne copie puis relancer `--copy`. Pour désinstaller, retirer uniquement le lien ou la copie `.agents/skills/vinted-prepare-listing` et conserver `skills/`.

## Vérification et tests

```sh
python3 tools/run_tests.py --report reports/tests-results.json
python3 tools/build_packages.py --check
```

Les tests vérifient les formats des archives, la concordance des manifestes, le document complet, les empreintes, les scénarios fictifs de prix et de provenance, ainsi que les outils locaux. Ils fonctionnent hors réseau, sans modèle, compte ni image réelle. Ils ne prouvent pas un import dans un compte Claude ou ChatGPT, ni le préremplissage réel de Vinted. Le [plan de validation](docs/VALIDATION.md) décrit les essais manuels par assistant et appareil.

La CI exécute la suite sous Linux, macOS et Windows avec Python 3.10 et 3.14, puis génère les paquets. La découverte locale Codex peut aussi être vérifiée, sans lancer de modèle :

```sh
python3 tools/verify_discovery.py
```

Cette commande facultative exige une CLI Codex installée. Elle contrôle les métadonnées du skill de ce projet et écrit sa preuve dans `livrables/installation-local.json`. Le serveur Codex peut initialiser ses fichiers d'état dans le profil utilisateur ; aucun compte Vinted n'est ouvert.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `skills/vinted-prepare-listing/` | Source commune des instructions et références. |
| `plugin.json` | Manifeste portable Agent Plugins pour ChatGPT/Codex. |
| `.claude-plugin/` | Manifeste Claude et catalogue importable depuis GitHub. |
| `docs/assistant-instructions.md` | Document mobile complet généré depuis le skill. |
| `tools/` | Génération des paquets, installation locale et vérification. |
| `tests/` | Scénarios fictifs et tests des outils et formats. |
| `docs/` | Plan de validation et revue du dépôt. |

Les photos, rapports d'exécution, documents de travail et installations locales restent hors du dépôt. Le projet n'est affilié ni à Vinted, ni à OpenAI, ni à Anthropic. Contributions : [CONTRIBUTING.md](CONTRIBUTING.md). Réutilisation : [licence MIT](LICENSE).

# VintedFastSelling

Préparer une annonce **Vinted France depuis ses photos**, sur téléphone avec ChatGPT ou Claude : titre, description et champs à recopier. Pour un vêtement ou un jouet à la fois. **Vous vérifiez et publiez vous-même.**

Le prix fourni par l'utilisateur est prioritaire. Sinon, l'assistant cherche une fourchette Vinted réellement visible et pertinente, puis des comparables sourcés si nécessaire. Il demande les informations utiles qui manquent et décrit les défauts connus.

## Démarrer dans ChatGPT sur téléphone

Cette page GitHub contient tout le texte à copier. La configuration se fait une fois dans les réglages de votre compte ChatGPT.

1. **Copier tout le bloc ci-dessous.** Utiliser le bouton de copie du bloc lorsqu’il est proposé, ou sélectionner son texte.
2. **[Ouvrir ChatGPT](https://chatgpt.com/)**, puis **Paramètres → Personnaliser ChatGPT → Instructions personnalisées**. Activer la personnalisation, coller le texte et enregistrer. Conserver vos autres préférences utiles dans la limite du champ.
3. **Ouvrir une nouvelle discussion**, joindre les photos de l’article et écrire **« Prépare ce produit pour Vinted »**. Ajouter le prix, la taille ou l’état si connus.

### Texte à copier

```text
Quand ma demande concerne Vinted, prépare une annonce en français et en EUR depuis mes photos d’un seul vêtement ou jouet.
Analyse les photos avant les questions. Garde seulement les faits visibles ou déclarés ; marque les inconnues, cite les défauts et regroupe les questions utiles. N’invente ni marque, taille, matière, état, fonctionnement ou accessoires. Conserve la taille exacte de l’étiquette.
Mon prix explicite prime. Sinon, retiens la borne haute d’une fourchette Vinted pertinente réellement visible ; à défaut, propose un prix à partir de comparables actuels avec liens. Sans source accessible, demande mon prix. N’invente aucune source ni estimation.
Fournis titre, description à copier, catégorie, marque, taille, état, couleur, prix et origine, ordre des photos et points à préciser.
« Prépare ce produit pour Vinted » = texte seul. « Vends ça sur Vinted » = préparation puis préremplissage seulement si les outils, la connexion et le transfert réel des photos sont disponibles. Sinon, donne la fiche à recopier. N’annonce aucun remplissage ou brouillon sauvegardé sans vérification. Ne publie jamais ; je publie moi-même. Ne demande aucun mot de passe ou code ; ne contourne aucun blocage.
Si le document complet des instructions Vinted est joint ou dans les fichiers du projet, consulte-le pour les règles détaillées.
```

Ce texte est autonome pour préparer une fiche ; le document complet mentionné à la dernière ligne est facultatif. Il fait moins de 1 500 caractères. Les instructions personnalisées sont disponibles sur iOS et Android avec toutes les offres ; leur limite documentée est de 1 500 caractères pour Free et Go, et de 5 000 pour les autres offres. [Guide officiel OpenAI](https://help.openai.com/fr-fr/articles/8096356-chatgpt-custom-instructions).

Le préremplissage de Vinted dépend des outils disponibles dans votre ChatGPT. Ces instructions permettent de préparer la fiche à recopier ; elles n’ajoutent pas de pilotage de l’app Vinted.

### Garder un espace dédié à Vinted

Vous pouvez aussi créer un **projet ChatGPT « Vinted »** et coller le même bloc dans **••• → Paramètres du projet**. Les instructions s’appliqueront aux discussions de ce projet. Pour disposer de toutes les règles détaillées, y ajouter le document complet proposé ci-dessous. [Guide officiel des projets](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

## Télécharger les documents

Les fichiers ci-dessous sont publiés dans les **Releases** de ce dépôt GitHub. Les ouvrir depuis le navigateur du téléphone, puis les enregistrer dans les fichiers de l’appareil.

| Fichier | Utilisation |
| --- | --- |
| [Instructions courtes à copier](https://github.com/Tereo/VintedFastSelling/releases/latest/download/chatgpt-custom-instructions.txt) | Le même texte que le bloc affiché ci-dessus. |
| [Document complet à joindre](https://github.com/Tereo/VintedFastSelling/releases/latest/download/vinted-prepare-listing-instructions.md) | Toutes les instructions et références dans un seul fichier, pour ChatGPT ou Claude. |
| [Tous les téléchargements](https://github.com/Tereo/VintedFastSelling/releases/latest) | Les documents et les archives pour les assistants compatibles. |

Pour utiliser le document complet dans ChatGPT ou Claude, le joindre avec les photos originales d’un article, puis écrire **« Applique les instructions jointes aux photos pour préparer mon annonce Vinted : titre, description et champs à recopier. »** Dans un projet ChatGPT, le document peut être ajouté une fois aux fichiers du projet ; le remplacer si vous souhaitez adopter une nouvelle version.

Le parcours principal consiste à copier le bloc de cette page ou à joindre le document téléchargé. Donner un lien à l’assistant ne garantit pas qu’il pourra en lire le contenu. Une URL GitHub ne modifie pas les réglages de votre compte ChatGPT : le collage de l’étape 2 reste nécessaire.

Les sources lisibles sur GitHub restent dans [docs/assistant-instructions.md](docs/assistant-instructions.md) et [docs/chatgpt-custom-instructions.txt](docs/chatgpt-custom-instructions.txt). La version courte résume les règles ; le document complet réunit le skill et toutes ses références et est généré depuis `skills/`. Le dépôt fournit aussi les formats de skill et plugin décrits ci-dessous.

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

## Télécharger ou générer les paquets

Pour télécharger les fichiers prêts à utiliser, ouvrir la [dernière version publiée](https://github.com/Tereo/VintedFastSelling/releases/latest), puis les fichiers de sa section **Assets**. Les documents et les ZIP y sont disponibles publiquement. Les ZIP d’importation pour Claude et les plugins concernent les assistants qui proposent ces fonctions ; le parcours ChatGPT mobile reste celui du début de cette page.

Les contributeurs peuvent aussi récupérer les fichiers d’une exécution CI : **Actions → Tests → une exécution réussie → Artifacts → vinted-claude-chatgpt**. Ces artefacts sont conservés 30 jours et leur téléchargement peut demander une connexion GitHub.

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

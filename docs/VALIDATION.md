# Valider le projet

## Contrôles automatiques

```sh
python3 tools/run_tests.py --report reports/tests-results.json
python3 tools/build_packages.py --check
```

Le rapport contient les résultats, la version de Python et les empreintes des fichiers du skill. Il est ignoré par Git. La CI applique cette commande sous Linux, macOS et Windows avec Python 3.10 et 3.14.

Les tests vérifient les données structurées des scénarios et l'outillage : installation sur un dossier neuf, copie en l'absence de liens symboliques, préservation d'une installation modifiée, échanges de métadonnées Codex et arrêt du processus en cas d'erreur ou de délai dépassé. Ils contrôlent aussi les racines des ZIP Claude et plugin, l'identité des fichiers embarqués, la concordance des versions, l'exclusion des fichiers locaux, la reproductibilité des empreintes et l'intégralité du document mobile. Les URLs `example.invalid`, articles, demandes et secrets de test sont fictifs.

Le banc n'appelle aucun modèle, ne lit pas d'image et ne lance pas Vinted. Un succès ne certifie pas la qualité de la rédaction libre, les décisions du modèle, le respect des instructions ni la compatibilité d'un navigateur réel.

## Paquets Claude et ChatGPT

```sh
python3 tools/build_packages.py
python3 tools/build_packages.py --check
```

La génération produit deux ZIP, un document unique et leurs empreintes dans `dist/`, ainsi que le document suivi dans `docs/assistant-instructions.md`. `--check` vérifie les sources et ce dernier sans écrire. La CI conserve les livrables téléchargeables pendant 30 jours après réussite de la matrice de tests.

Avec une CLI Claude Code compatible, vérifier le plugin et son catalogue sans installer le plugin ni exécuter de modèle :

```sh
claude plugin validate .
```

Les manifestes suivent les [formats OpenAI](https://developers.openai.com/plugins/build/plugins) et [Claude](https://code.claude.com/docs/en/plugins/manifest-reference). Le ZIP du skill suit [le format d'import Claude](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills). Une validation du format ne démontre pas que l'import est proposé ou activé sur un compte donné.

Les essais suivants restent à conduire avec un compte et un appareil réels. Ne marquer une case comme réussie qu'après observation de l'import et du résultat, sans publier une annonce :

| Surface | Essai manuel attendu |
| --- | --- |
| Claude, interface d'import Skills | Importer `vinted-prepare-listing-claude.zip`, activer le skill et observer le chargement de ses références. |
| Claude avec plugins | Ajouter le dépôt par l'interface de marketplace disponible, installer le plugin et vérifier qu'une seule instance du skill est chargée. |
| Claude sur iOS et Android | Fournir les photos avec le skill activé ou le document complet joint ; demander une fiche et relever le parcours réellement disponible. |
| ChatGPT avec import de plugins autorisé | Importer le catalogue GitHub depuis les réglages administrateur, rendre le plugin disponible et le sélectionner dans une nouvelle conversation. |
| ChatGPT sur iOS et Android | Utiliser le plugin disponible ou le document complet joint avec les photos ; vérifier la lecture des références et une fiche sans invention. |
| Claude et ChatGPT, document joint | Demander l'application du document sans annoncer une installation durable ou une mémoire entre chats. |
| Claude et ChatGPT, lien inaccessible | L'assistant demande le document complet, conserve les informations déjà reçues et ne prétend pas avoir lu les références absentes. |

Pour le préremplissage, vérifier séparément les outils, la connexion Vinted et le transfert réel des photos sur chaque assistant et appareil. Le document ou le skill n'apporte pas ces outils.

## Installation et découverte

Depuis une copie neuve du dépôt, sans `.agents/` ni `livrables/` :

```sh
python3 tools/install_local.py
python3 tools/install_local.py --check
python3 tools/verify_discovery.py
```

La dernière commande est facultative et exige une CLI Codex compatible. Vérifier la découverte d'une seule instance activée du skill de ce projet. Le rapport d'installation est une preuve locale ; il ne valide ni un compte Vinted, ni un import dans Claude ou ChatGPT, ni une surface mobile.

## Essais avec l'agent et le navigateur

Ces essais utilisent les photos et le compte de la personne qui les demande. Ils restent à conduire dans chaque environnement cible. Consigner une preuve minimale sans identifiant de compte, URL privée, secret ou photo personnelle dans le dépôt.

| Cas | Résultat à observer |
| --- | --- |
| Photos + « vends ça sur Vinted » ou « vend ca sur vinted » | Skill reconnu sans son nom ; fiche puis préremplissage si disponible, publication laissée à l’utilisateur. |
| Photos + « prépare ce produit pour Vinted » | Skill reconnu sans son nom ; texte et champs à recopier, sans ouverture de Vinted. |
| Photos + « vends ça sur Vinted à 12,50 €. Porté deux fois. » | Prix conservé et état déclaré pris en compte sans demander de reformuler la commande. |
| « Vends ça sur Vinted, texte seulement » / « prépare ce produit pour Vinted et préremplis Vinted » | La précision explicite choisit respectivement le texte seul / le préremplissage. |
| Vêtement, étiquette lisible, prix `12,50 €` | Taille exacte, prix conservé, défauts décrits. |
| Jouet incomplet ou non testé | Pièces manquantes explicites, questions sur les accessoires et le fonctionnement. |
| Étiquette illisible ou contradiction | Information laissée inconnue et question utile, sans invention. |
| Aucun prix utilisateur | Suggestion Vinted pertinente réellement visible ; à défaut, comparables datés puis question si insuffisants. |
| Préparation hors site | Fiche fournie sans ouverture de Vinted. |
| Navigateur ou transfert indisponible | Fiche conservée, limitation précise, aucun faux succès de préremplissage. |
| Session expirée | Connexion par l'utilisateur dans l'interface sécurisée, reprise après observation. |
| Brouillon existant ou interruption | Contrôle des doublons, relecture, accord pour modifier un contenu existant. |
| CAPTCHA ou restriction rencontré | Main à l'utilisateur ou arrêt ; aucune relance de contournement. |
| Formulaire rempli | Titre, description, attributs, état, colis, prix et vignettes relus. |
| Brouillon sauvegardé | Présence persistante ou réouverture constatée avec valeurs et photos. |
| Reprise sur iOS ou Android | Instructions, outils et brouillon réellement accessibles dans l'assistant, le compte et l'appareil cibles. |

Ne jamais activer la publication, un achat ou une option payante lors de ces essais. La validation du parcours complet nécessite les observations réelles correspondant au résultat annoncé.

# Valider le projet

## Contrôles automatiques

```sh
python3 tools/run_tests.py --report reports/tests-results.json
```

Le rapport contient les résultats, la version de Python et les empreintes des fichiers du skill. Il est ignoré par Git. La CI applique cette commande sous Linux, macOS et Windows avec Python 3.10 et 3.14.

Les tests vérifient les données structurées des scénarios et l'outillage : installation sur un dossier neuf, copie en l'absence de liens symboliques, préservation d'une installation modifiée, échanges de métadonnées Codex et arrêt du processus en cas d'erreur ou de délai dépassé. Les URLs `example.invalid`, articles, demandes et secrets de test sont fictifs.

Le banc n'appelle aucun modèle, ne lit pas d'image et ne lance pas Vinted. Un succès ne certifie pas la qualité de la rédaction libre, les décisions du modèle, le respect des instructions ni la compatibilité d'un navigateur réel.

## Installation et découverte

Depuis une copie neuve du dépôt, sans `.agents/` ni `livrables/` :

```sh
python3 tools/install_local.py
python3 tools/install_local.py --check
python3 tools/verify_discovery.py
```

La dernière commande est facultative et exige une CLI Codex compatible. Vérifier la découverte d'une seule instance activée du skill de ce projet. Le rapport d'installation est une preuve locale ; il ne valide ni un compte Vinted, ni une distribution par plugin, ni Android.

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
| Reprise sur Android | Installation, outils et brouillon réellement accessibles sur le compte et l'appareil cible. |

Ne jamais activer la publication, un achat ou une option payante lors de ces essais. La validation du parcours complet nécessite les observations réelles correspondant au résultat annoncé.

# Navigateur autorisé et reprise

## Portes de faisabilité

Pour chaque point effectivement vérifié, noter dans la conversation la date, la surface, les versions visibles si disponibles, le résultat et une preuve minimale non sensible. Ne jamais inventer une version ou transformer un scénario simulé en vérification réelle.

- G1 : inventorier les outils documentés réellement disponibles, la surface cloud ou bureau choisie et la réception des photos. Une installation locale ne prouve ni l’accès au skill sur Android ni sa distribution sur le compte. Ne pas installer d’extension Android ni supposer Chrome mobile pilotable.
- G2, révisé à la demande de l’utilisateur : la demande de préparer l’annonce avec ce skill autorise le navigateur et le préremplissage de l’article concerné sur son compte, y compris les photos fournies, la recherche de prix utile et la sauvegarde en brouillon lorsqu’elle existe. Une demande de fiche hors site seule exclut ces interactions. Respecter le périmètre déjà autorisé sans redemander un accord ni une preuve distincte émanant de Vinted. Cette règle ne prétend pas établir une autorisation contractuelle de la plateforme et ne permet aucun contournement d’une restriction constatée.
- G3 : pendant le parcours demandé, vérifier connexion sécurisée, accès au formulaire, transfert réel des photos et conservation observable pour reprise manuelle. Un point non testé signifie parcours non validé ; une étape tentée sans succès signifie résultat partiel. Une demande de l’utilisateur de reprendre l’essai ici autorise la poursuite de cet essai dans l’environnement courant.

Le skill n’apporte pas de navigateur absent. Découvrir et employer exclusivement ses commandes documentées, sans sélecteur deviné ni coordonnées fixes. Ne jamais utiliser d’API Vinted privée, de cookies exportés ou d’accès au stockage de session.

## Connexion

Observer les éléments visibles du compte et l’accès vendeur. L’URL, un chargement de page ou la déclaration « je suis connecté » ne suffisent pas à vérifier la session.

Si déconnecté, ouvrir le parcours officiel et rendre la main dans l’interface sécurisée disponible sur la surface choisie. Ne demander, lire ou journaliser aucun mot de passe, code MFA, cookie ou jeton. Reprendre seulement après observation du compte et du formulaire. Si la connexion nécessite un ordinateur inaccessible à l’utilisateur Android, annoncer le blocage.

CAPTCHA, MFA et contrôle d’identité nécessitent la main de l’utilisateur. Une restriction, un refus d’automatisation ou une modération provoquent l’arrêt des actions ; aucune relance automatique, usurpation de navigateur ou résolution par un service tiers. Ne reprendre qu’après résolution réelle et nouvelle observation, dans la limite de l’autorisation G2.

## Cadence du préremplissage

Préparer les textes et valeurs hors du formulaire avant de saisir. Conserver la session et l’onglet déjà ouverts pour cet article ; ne pas recréer une session à chaque champ. Ne saisir que les valeurs manquantes ou réellement différentes, après lecture de l’état courant.

- Effectuer une seule interaction de modification à la fois dans le formulaire. Attendre son résultat avant la suivante ; ne pas paralléliser les saisies ni les téléversements sur cet article.
- Entre deux saisies de champs, ajouter une pause aléatoire bornée de 1 à 3 secondes, uniquement avec un générateur d’aléa et une commande d’attente documentés déjà disponibles dans l’environnement. Tirer une nouvelle durée à chaque intervalle ; ne pas utiliser une suite fixe présentée comme aléatoire. Ne pas installer de dépendance pour cette seule fonction. Si l’une de ces capacités manque, conserver les actions séquentielles et les vérifications, et signaler que la pause aléatoire n’a pas pu être appliquée.
- Après un choix de catégorie, attendre l’affichage des champs dépendants et relire les options avant la saisie suivante. Après un transfert de photos, attendre la fin du transfert et contrôler les vignettes. Une pause chronométrée ne remplace jamais ces observations.
- Employer les interactions de l’outil disponible avec les champs observés. Ne pas remplir tous les champs par injection de script, ajouter des frappes erronées, des clics ou des mouvements factices pour simuler une personne. Temporiser localement, sans rafraîchir Vinted ni multiplier les requêtes pour occuper l’attente.
- Si une attente d’interface n’aboutit pas dans la limite documentée de l’outil, observer l’état et appliquer la reprise bornée ci-dessous. Un CAPTCHA ou une restriction interrompt immédiatement la séquence, y compris une éventuelle pause en cours lorsque l’outil permet cette interruption.

La plage de 1 à 3 secondes est un réglage local de cadence, sans efficacité anti-détection démontrée sur Vinted. Les signaux du navigateur, du réseau et du compte ne sont pas contrôlés par ces instructions. Un skill de navigation tiers ne change ces capacités que si son moteur est réellement disponible et compatible ; ne pas annoncer une fonction « stealth » à partir de sa seule installation. Conserver les règles de connexion et d’arrêt ci-dessus.

## Doublons et premier remplissage

Avant une création, examiner les brouillons et annonces pertinents si l’interface autorisée le permet. En cas de résultat ambigu, demander clarification avant toute création. Si l’examen n’est pas possible, le signaler et demander à l’utilisateur si un brouillon ou une annonce existe déjà. Une correspondance trouvée ne vaut pas autorisation de modifier un contenu existant. Demander l’accord correspondant, sans supprimer ni republier. Vérifier à nouveau l’état existant après une interruption ou une connexion rétablie.

Vérifier par un accès autorisé les règles du catalogue en vigueur pour la catégorie et les images. Si l’éligibilité de l’article ou d’une photo reste incertaine, signaler le point avant le remplissage ; ne pas choisir une catégorie pour contourner une restriction.

Observer les options et champs obligatoires courants. Choisir une catégorie précise et relire ses dépendances : marque, taille ou attributs, état, éventuelle suggestion de prix et colis. Ne saisir que les valeurs établies ou propositions dont l’arbitrage est résolu ; conserver les questions ouvertes. Lire le prix selon [pricing.md](pricing.md), sans montant temporaire.

Vérifier que les pièces jointes accessibles à la vision sont aussi transférables avec l’outil exposé. Vision et téléversement sont deux capacités distinctes. Utiliser uniquement les photos de l’article, dans l’ordre retenu et dans la limite observée. Contrôler l’identité des vignettes, leur nombre et leur ordre ; une commande d’upload réussie ne suffit pas. Si le transfert échoue, préserver la fiche, décrire ce qui manque et laisser la jonction manuelle à l’utilisateur. Ne pas retransférer aveuglément des images déjà présentes.

## Relecture, sauvegarde et arrêt

Relire le titre, la description complète, la catégorie, tous les attributs requis, l’état, le colis et le prix. Comparer avec la fiche et les photos prévues. Un champ masqué ou non vérifié empêche d’annoncer un formulaire vérifié. Si la sauvegarde du brouillon n’est pas explicitement distincte d’une publication, ne pas activer le bouton ambigu.

Sauvegarder seulement si une fonction de brouillon existe réellement. Déclarer « brouillon vérifié » uniquement après constat de sa présence persistante ou réouverture avec contrôle des valeurs et photos. Sinon annoncer « formulaire vérifié » ou « formulaire partiel », et préciser que la persistance et la reprise depuis Chrome Android ne sont pas garanties. Ne pas présenter l’URL privée comme un lien public.

Ne jamais activer Publier ou une commande équivalente. La publication manuelle reste à l’utilisateur, même si une demande ultérieure emploie « vas-y », « termine » ou « publie ». Ne pas activer de promotion ou d’option payante.

## Incident et reprise

Une reprise commence par une observation de l’interface et de la fiche ; relire ce qui est déjà saisi, les photos et les éventuels brouillons. Pour une panne transitoire, autoriser une seule nouvelle tentative après cette observation et seulement si l’effet à retenter est clairement connu. Si une création ou sauvegarde a un résultat ambigu, rechercher d’abord ce qui existe ; sans conclusion, arrêter et demander à l’utilisateur. Pas de boucle de relance devant CAPTCHA, restriction ou modération. Conserver le résultat partiel et la prochaine action utile.

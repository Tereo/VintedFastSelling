# Contribuer

Les instructions sont dans `skills/`, les outils Python dans `tools/` et les scénarios fictifs dans `tests/`. Python 3.10 ou supérieur et sa bibliothèque standard suffisent.

Avant une proposition de modification, lancer :

```sh
python3 tools/run_tests.py
python3 tools/build_packages.py --check
```

Pour une correction de comportement, ajouter un cas qui reproduit le problème. Distinguer les observations réelles des simulations : le banc n'exécute ni modèle ni navigateur. Si le parcours évolue, mettre à jour [le plan de validation](docs/VALIDATION.md).

Conserver la priorité du prix utilisateur, la provenance des informations, les défauts connus et la publication manuelle. Tester l'installation sur une copie propre du dépôt après modification des outils ; la CI couvre Linux, macOS et Windows.

Les instructions communes à Claude et ChatGPT restent dans `skills/`. Après modification, lancer `python3 tools/build_packages.py` et inclure la mise à jour générée de `docs/assistant-instructions.md` dans la proposition. Ne pas modifier ce document à la main ni ajouter les ZIP de `dist/` au dépôt. Garder les identités et versions de `plugin.json` et `.claude-plugin/plugin.json` cohérentes. Le catalogue `.claude-plugin/marketplace.json` pointe vers ce plugin unique à la racine.

Utiliser uniquement des données fictives dans les tests. Les photos, documents de travail, rapports locaux, cookies, jetons, fichiers `.env` et fichiers de configuration personnels ne doivent pas être ajoutés aux commits. Les dossiers prévus pour ces fichiers sont décrits dans `.gitignore`. Toute donnée réelle utile à un diagnostic doit être remplacée par un exemple anonymisé.

Les contributions sont proposées sous la [licence MIT](LICENSE) du projet.

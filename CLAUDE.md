# Je danse en ligne (delmtl.ca)

Site statique (GitHub Pages) qui répertorie les soirées et cours de danse en ligne du Grand Montréal.
Toutes les données sont dans `donnees.json`.

## Fonctionnement

- Un push sur `main` qui modifie `donnees.json` déclenche `.github/workflows/sync-sheets.yml` :
  1. les onglets « Soirées » et « Cours » du Google Sheet « Je danse en ligne » sont **entièrement remplacés** par le contenu de `donnees.json` ;
  2. `generer_statique.py` régénère `evenements.html`, puis le bot le pousse sur `main`.
- Le workflow ne tourne que sur `main` : une branche de travail ne peut pas écraser le Google Sheet.
- Après un push sur `main`, faire `git pull origin main` avant le push suivant (le bot ajoute un commit `evenements.html`).

## Règle permanente : ajout d'un événement

Quand l'utilisatrice ou l'utilisateur envoie une affiche ou une info d'événement :

1. Structurer l'info et l'ajouter à `donnees.json` (`soirees` ou `cours`) en respectant le format existant.
2. Demander **seulement** ce qui manque d'essentiel (heure, prix, dates). Ne rien inventer.
3. Valider le JSON, committer et pousser **directement sur `main`**.
4. Confirmer en une seule phrase.

Communication : français du Québec, vouvoiement, termes épicènes, espace avant les deux points mais pas avant `!`, `?` ou `;`.

### Format des entrées

Écrire le fichier avec `json.dump(data, f, ensure_ascii=False, indent=2)`. Toutes les clés sont présentes dans chaque entrée ; une valeur inconnue est une chaîne vide `""`.

**`soirees`** : `Type`, `Organisateur`, `Association`, `Lieu / Centre`, `Adresse`, `Récurrent`, `Jour(s)`, `Heure début`, `Heure fin`, `Date début`, `Date fin`, `Prix`, `Précisions`, `URL source`, `URL association`, `Saison`, `Lieu type`

**`cours`** : `Organisateur`, `Association`, `Lieu / Centre`, `Adresse`, `Jour(s)`, `Heure début`, `Heure fin`, `Date début`, `Date fin`, `Prix`, `Niveau`, `Précisions`, `URL source`, `URL association`, `Saison`, `Lieu type`

Conventions :
- `Type` (soirées) : `En ligne`, `En ligne + sociale`, `Ponctuelle` ou `Récurrente`.
- `Récurrent` : `Oui` ou `Non`. Pour une date unique, `Date début` = `Date fin`.
- `Jour(s)` : `Lundi` … `Dimanche` (majuscule initiale).
- Heures : `19h30`, `21h00`. Dates : `AAAA-MM-JJ`.
- Prix : `10$`, `Gratuit`, `75$ / 10 cours`.
- `Saison` : `Hiver AAAA`, `Printemps AAAA`, `Été AAAA` ou `Automne AAAA` (doit exister dans `ORDRE_SAISONS` de `generer_statique.py`).
- `Lieu type` : `Intérieur` ou `Extérieur`.
- Message de commit descriptif, p. ex. « Ajout soirée Sono danse 15 novembre Terrebonne ».

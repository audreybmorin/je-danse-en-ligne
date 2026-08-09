#!/usr/bin/env python3
"""
Génère evenements.html — page statique lisible par Google sans JavaScript.
Appelé par GitHub Actions après chaque mise à jour de donnees.json.
"""
import json, sys
from datetime import date

with open('donnees.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

aujourd_hui = date.today()

MOIS = ['jan.','fév.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.']

def fmt_date(d):
    if not d: return ''
    try:
        y, m, j = d.split('-')
        return f"{int(j)} {MOIS[int(m)-1]} {y}"
    except:
        return d

def est_actuel(ev):
    fin = ev.get('Date fin') or ev.get('Date début')
    if not fin: return True
    try:
        y, m, j = fin.split('-')
        return date(int(y), int(m), int(j)) >= aujourd_hui
    except:
        return True

ORDRE_SAISONS = [
    'Printemps 2025','Été 2025','Automne 2025','Hiver 2026','Printemps 2026',
    'Été 2026','Automne 2026','Hiver 2027','Printemps 2027','Été 2027',
    'Automne 2027','Hiver 2028','Printemps 2028','Été 2028'
]

# Filtrer les entrées actuelles
soirees = [e for e in data['soirees'] if est_actuel(e)]
cours   = [e for e in data['cours']   if est_actuel(e)]

# Grouper par saison
par_saison = {}
for ev in soirees:
    s = ev.get('Saison', 'Non classé')
    par_saison.setdefault(s, {'soirees': [], 'cours': []})['soirees'].append(ev)
for ev in cours:
    s = ev.get('Saison', 'Non classé')
    par_saison.setdefault(s, {'soirees': [], 'cours': []})['cours'].append(ev)

saisons_presentes = [s for s in ORDRE_SAISONS if s in par_saison]

html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Événements et cours de danse en ligne sociale — Grand Montréal | DELmtl</title>
<meta name="description" content="Liste complète des cours, ateliers, soirées et événements de danse en ligne sociale dans le Grand Montréal. Mis à jour régulièrement.">
<link rel="canonical" href="https://delmtl.ca/evenements.html">
<style>
  body { font-family: sans-serif; max-width: 900px; margin: 0 auto; padding: 1rem 1.5rem; color: #1a1a2e; }
  h1 { color: #E8175D; }
  h2 { background: #1a1a2e; color: white; padding: .4rem .8rem; border-radius: 4px; font-size: 1rem; margin: 2rem 0 .75rem; }
  h3 { color: #5C5C7A; font-size: .8rem; text-transform: uppercase; letter-spacing: 1px; margin: 1.25rem 0 .5rem; border-bottom: 1px solid #e0e0ec; padding-bottom: .25rem; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: .9rem; }
  th { background: #f0f0f8; text-align: left; padding: .4rem .6rem; font-size: .8rem; }
  td { padding: .4rem .6rem; border-bottom: 1px solid #f0f0f8; vertical-align: top; }
  .badge { display: inline-block; padding: 1px 6px; border-radius: 10px; font-size: .75rem; font-weight: 600; }
  .soiree { background: #e0f2f1; color: #00695c; }
  .cours  { background: #ede7f6; color: #4527a0; }
  .sociale{ background: #fff3e0; color: #e65100; }
  .ext    { background: #e8f5e9; color: #2e7d32; }
  .int    { background: #e3f2fd; color: #1565c0; }
  .gratuit{ background: #e0f2f1; color: #00695c; font-weight: 700; }
  nav { margin: 1rem 0 2rem; }
  nav a { color: #E8175D; }
  footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e0e0ec; font-size: .8rem; color: #888; }
</style>
</head>
<body>
<nav><a href="/">← Retour à DELmtl.ca</a></nav>
<h1>Événements et cours de danse en ligne sociale</h1>
<p>Répertoire complet des activités de danse en ligne sociale dans le Grand Montréal, mis à jour régulièrement. Pour une expérience optimale avec filtres et vue interactive, visitez <a href="/">DELmtl.ca</a>.</p>
'''

for saison in saisons_presentes:
    html += f'<h2>{saison}</h2>\n'
    groupe = par_saison[saison]

    # Soirées ponctuelles
    ponc = sorted([e for e in groupe['soirees'] if e.get('Récurrent') != 'Oui'],
                  key=lambda e: e.get('Date début',''))
    # Soirées récurrentes
    rec  = sorted([e for e in groupe['soirees'] if e.get('Récurrent') == 'Oui'],
                  key=lambda e: ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'].index(e.get('Jour(s)','')) if e.get('Jour(s)') in ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'] else 99)

    if ponc or rec:
        html += '<h3>Soirées et événements</h3>\n<table>\n'
        html += '<tr><th>Date / Jour</th><th>Organisateur</th><th>Lieu</th><th>Heure</th><th>Prix</th><th>Type</th></tr>\n'
        for ev in ponc + rec:
            date_str = fmt_date(ev.get('Date début','')) if ev.get('Récurrent') != 'Oui' else ev.get('Jour(s)','')
            if ev.get('Récurrent') == 'Oui' and ev.get('Date début') and ev.get('Date fin'):
                date_str += f" ({fmt_date(ev.get('Date début'))} au {fmt_date(ev.get('Date fin'))})"
            org = ev.get('Organisateur') or ev.get('Lieu / Centre','')
            lieu = ev.get('Lieu / Centre','')
            if ev.get('Adresse'): lieu += f', {ev["Adresse"]}'
            heure = ev.get('Heure début','')
            if ev.get('Heure fin'): heure += f' à {ev["Heure fin"]}'
            prix = ev.get('Prix','')
            type_badge = 'sociale' if ev.get('Type') == 'En ligne + sociale' else 'soiree'
            type_label = '+ sociale' if ev.get('Type') == 'En ligne + sociale' else 'En ligne'
            lieu_type = ev.get('Lieu type','')
            lieu_badge = f'<span class="badge ext">🌳</span> ' if lieu_type == 'Extérieur' else '<span class="badge int">🏠</span> ' if lieu_type == 'Intérieur' else ''
            prix_badge = f'<span class="badge gratuit">{prix}</span>' if prix.lower() == 'gratuit' else prix
            prec = ev.get('Précisions','')
            html += f'<tr><td>{date_str}</td><td>{org}</td><td>{lieu_badge}{lieu}{("<br><small>"+prec+"</small>") if prec else ""}</td><td>{heure}</td><td>{prix_badge}</td><td><span class="badge {type_badge}">{type_label}</span></td></tr>\n'
        html += '</table>\n'

    # Cours
    cours_s = sorted(groupe['cours'], key=lambda e: e.get('Date début',''))
    if cours_s:
        html += '<h3>Cours et ateliers</h3>\n<table>\n'
        html += '<tr><th>Date / Jour</th><th>Organisateur</th><th>Lieu</th><th>Heure</th><th>Prix</th><th>Niveau</th></tr>\n'
        for ev in cours_s:
            date_str = ev.get('Jour(s)','')
            if ev.get('Date début') and ev.get('Date fin'):
                date_str += f' ({fmt_date(ev.get("Date début"))} au {fmt_date(ev.get("Date fin"))})'
            org = ev.get('Organisateur','')
            lieu = ev.get('Lieu / Centre','')
            if ev.get('Adresse'): lieu += f', {ev["Adresse"]}'
            heure = ev.get('Heure début','')
            if ev.get('Heure fin'): heure += f' à {ev["Heure fin"]}'
            prix = ev.get('Prix','')
            prix_badge = f'<span class="badge gratuit">{prix}</span>' if prix.lower() == 'gratuit' else prix
            niveau = ev.get('Niveau','')
            lieu_type = ev.get('Lieu type','')
            lieu_badge = f'<span class="badge ext">🌳</span> ' if lieu_type == 'Extérieur' else '<span class="badge int">🏠</span> ' if lieu_type == 'Intérieur' else ''
            prec = ev.get('Précisions','')
            html += f'<tr><td>{date_str}</td><td>{org}</td><td>{lieu_badge}{lieu}{("<br><small>"+prec+"</small>") if prec else ""}</td><td>{heure}</td><td>{prix_badge}</td><td>{niveau}</td></tr>\n'
        html += '</table>\n'

html += f'''<footer>
  <p>DELmtl.ca — Répertoire de la danse en ligne sociale dans le Grand Montréal<br>
  Page générée automatiquement. Données mises à jour régulièrement.<br>
  <a href="/">Retour à l'accueil</a> | <a href="/a-propos.html">À propos</a></p>
</footer>
</body>
</html>'''

with open('evenements.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"OK — {len(soirees)} soirées, {len(cours)} cours")

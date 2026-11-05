# Orchestrateur ou integration continue ? (TP06)

| Critere                           | Prefect (orchestrateur) | GitHub Actions (CI) |
|-----------------------------------|-------------------------|---------------------|
| Ce qui declenche l'execution      | Une planification cron (`0 6 * * 1`, chaque lundi 6 h), un Quick run depuis l'interface, ou `python flow_mlops.py` | Un evenement Git : chaque `git push` (ou le bouton "Run workflow" via `workflow_dispatch`) |
| Ou s'execute le traitement        | Sur notre poste / serveur : le processus `serve` ou le worker du work pool `pool-tp`, avec acces aux donnees reelles (`dvc-stockage`) | Sur une machine Linux ephemere de GitHub (`ubuntu-latest`), sans acces au stockage DVC local (donnees regenerees) |
| Qui surveille, et ou              | L'equipe data / MLOps, dans l'interface Prefect (http://127.0.0.1:4200) : runs, etat de chaque tache, durees, journaux | Les developpeurs, dans l'onglet Actions du depot et via la croix rouge / coche verte sur chaque commit |
| Ce qui se passe en cas d'echec    | La tache fautive passe en Failed (reessais automatiques pour `rejouer_pipeline`), le flow run est Failed, `notifier` n'est pas executee : le modele n'est pas promu | L'etape `verifier_qualite.py` sort avec le code 1, le job devient rouge, le commit est marque en echec ; on corrige ou on fait `git revert` |
| Type de tache adapte              | Traitements recurrents et longs sur les donnees : reentrainement, scoring batch, ingestion, avec dependances entre taches | Verifications rapides et reproductibles du code a chaque modification : tests, lint, pipeline sur donnees de reference, regle de qualite |
| Ce qui est versionne dans Git     | Le workflow (`flow_mlops.py`), sa planification (`planifier.py`, `prefect.yaml`) ; l'historique des runs reste dans la base Prefect, hors Git | La definition de la chaine (`.github/workflows/ci.yml`), `verifier_qualite.py`, `requirements-ci.txt` ; les resultats des runs restent sur GitHub |

## Conclusion (5 lignes)

La CI (GitHub Actions) valide le code : chaque `git push` rejoue le pipeline et refuse un commit qui fait tomber le F1 sous 0.82.
L'orchestrateur (Prefect) execute et surveille des traitements recurrents : reentrainement chaque lundi a 6 h, sur les vraies donnees.
Dans les deux cas, la meme regle de qualite (`seuil_f1` de `params.yaml`) bloque un modele degrade (F1 = 0.25 avec `max_depth: 2`).
La CI agit avant que le changement atteigne la production ; l'orchestrateur agit pendant la vie du modele en production.
Les deux sont complementaires : aucun ne remplace l'autre, et tous deux sont decrits dans des fichiers versionnes.

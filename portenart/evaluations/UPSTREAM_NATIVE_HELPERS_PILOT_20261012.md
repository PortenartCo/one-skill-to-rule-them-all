# Portenart — pilote isole des scripts originaux Task Observer

Date de rapport : 12 octobre 2026 (Europe/Brussels)

## Verdict

**UPSTREAM_HELPERS_SYNTHETIC=PASS — 36/36 verifications**, au sein d'un bac a sable distinct des environnements metier. **TRUE_CODEX_ACTIVATION=NOT_TESTED ; PORTENART_INTEGRATION=NO_GO**.

## Source testee

Fork public : `PortenartCo/one-skill-to-rule-them-all` ; snapshot source originel lu au commit `07a7d926ad986548b8d5dac1db9fc9687c0060ef`. Trois scripts **originaux, non modifies**, copies de facon byte-identique et verifies avec l'empreinte Git blob SHA-1 :

| Script original | Empreinte Git blob SHA-1 |
| --- | --- |
| `scripts/new-observation.sh` | `9ce7d716c9faef8f7b1c8ad65065e01006dd7224` |
| `scripts/session-start-scan.sh` | `090aa2dfb8fd870ca39958ea0f383c94466d02b2` |
| `scripts/skill-load.sh` | `5339b9b5dc3f7d37797f8e739336b395382b47d6` |

La Skill amont se presente comme `task-observer` v3.6.0. Le code source est sous licence CC BY 4.0 ; attribution : Eoghan Henn et contributeurs, `rebelytics/one-skill-to-rule-them-all`.

## Protocole reel effectue

- Initialisation d'un journal **entierement fictif** dans un repertoire temporaire dont le chemin contient des espaces.
- Execution du script amont `session-start-scan.sh` sur un journal vide, puis apres creation d'observations.
- Creation de trois observations par l'original `new-observation.sh` ; numerotation 0001, 0002, 0003 et plancher d'identifiants conserve.
- Ecriture de l'entete YAML et du contenu textuel **synthetiques uniquement** dans les fichiers emis par le script d'origine.
- Lecture de l'entete du journal par le scanner, sans reprise du marqueur place volontairement dans le corps.
- Recherche ciblee d'observations ouvertes par le script amont `skill-load.sh`, y compris avec nom de Skill qualifie ; une Skill sans observation ouverte retourne 0.
- Passage d'une observation fictive au statut `actioned`, date de resolution fictive ancienne, puis archivage lors de la creation suivante.
- Refus d'un slug invalide par le script de creation.
- Quatre creations simultanees dans un **second journal fictif** : codes de sortie zero, identifiants distincts, plancher non regresse.
- Controle d'un journal `checkpoints.log` alimente par les appels de scan et de chargement.

**Resultat : 36 points de controle reussis sur 36, aucun echec.** Les scripts ont ete executes comme des processus distincts ; les fichiers factices ont ete retrouves apres leur terminaison. Le banc portable Python, valide sur les memes scripts, est publie dans [`portenart/tests/upstream-native-smoke.py`](../tests/upstream-native-smoke.py) et renvoie `PASS`, `checks=36`, `failed=0`, `sandbox_removed=true`. Un second banc Bash local a egalement retourne `UPSTREAM_NATIVE_SMOKE=PASS`. **Le banc Python portable a ensuite ete relance trois fois de suite : 36/36 PASS a chaque passage**, avec suppression de son repertoire temporaire confirmee a chaque fois. La source Python publiee et celle executee sont byte-identiques (Git blob `b7df06d4ba7557d6339609bdc8aafb4ad023d5b8`).

## Reproduction depuis le depot GitHub

Depuis le checkout de cette PR, sous Linux avec Bash, Python 3 et les outils POSIX usuels :

```sh
python3 portenart/tests/upstream-native-smoke.py
```

Le banc n'installe aucune dependance, invoque les scripts originaux dans des processus recevant un environnement minimal explicite, cree ses seuls journaux fictifs dans `/tmp` et supprime le repertoire temporaire apres execution. N'utilise aucun email, aucune source Portenart reelle, aucune API.

## Controle de risque

- Repertoire de travail et observations exclusivement temporaires, crees dans le bac a sable du modele ; aucune donnee metier, aucun mail, aucun fichier SharePoint, aucun compte ni secret Portenart employe.
- Processus enfants demarres avec un environnement explicitement minimal : `PATH`, `HOME`, `LANG`, `TZ`, `TMPDIR`, sans passage des variables de jetons/API.
- Aucune requete reseau, aucun connecteur, aucun hook, aucune installation de Skill, aucun fichier utilisateur modifie.
- Les scripts amont ecrivent **intentionnellement** le journal et les checkpoints, mais seulement a l'interieur du bac a sable cible dans ce pilote ; ce ne sont pas des scripts purement read-only.
- Aucun historique operationnel n'a ete exporte ni pousse dans un depot public. Les fichiers fictifs du bac a sable n'ont aucune portee probatoire metier.

## Ce que la preuve ne demontre PAS

1. **Activation automatique** de `task-observer` a l'ouverture d'une session Codex, ChatGPT ou autre agent.
2. Observation d'une conversation **reelle** par une Skill, qualite du jugement semantique du modele ou detection fiable de corrections sans instruction explicite.
3. Persistance inter-sessions Cloud, gouvernance de la retention, chiffrement, relecture et migration des journaux, synchronisation multi-agents ou autorisations en production.
4. Workflow de revue humaine complet, mise a jour de Skills et verifications d'absence de duplication avec les proprietaires `diagnostic-portenart` et `apprentissage-operationnel-portenart`.
5. Validation des deux autres scripts amont (`migrate-log.py` et `validate-skill-bundle.py`) ou d'une activation via hook.
6. Certification du perimetre d'isolation Codex Cloud : la recette Cloud demeure `REVIEW_NOT_RUN` compte tenu des controles reseau/identites/permissions insuffisamment attestes.

## Prochaine etape techniquement utile

Un **pilote agent explicite et optionnel**, dans un environnement prive sans credentials ni connecteurs et sans agents Portenart, comportant deux sessions distinctes, sur un corpus de travail integralement invente. La premiere suivrait vraiment le protocole `SKILL.md` (sans hook permanent), ecrirait une proposition fictive ; la seconde prouverait une relecture independante du journal. Verifier provenance, quotas et retention avant toute persistance hors du test. Aucune observation personnelle, Skill existante ou source de verite Portenart ne doit etre utilisee.

**Gate** : poursuite du cadrage et des essais fictifs locaux autorisee ; aucun branchement permanent, aucune installation globale, aucun transfert de donnees reelles, aucun merge et aucune activation de production.
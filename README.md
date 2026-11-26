# Lab Toolkit
[![CI](https://github.com/amine-guissouma/lab-toolkit/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/amine-guissouma/lab-toolkit/actions/workflows/ci.yml)
![Version 0.1.0 WIP](https://img.shields.io/badge/version-0.1.0%20WIP-orange.svg)
![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)


Développement destiné aux différents dépôts des laboratoires (`lab-*`).

`lab-toolkit` fournit une interface en ligne de commande permettant de vérifier et de gérer certaines configurations propres aux projets des laboratoires, notamment les paramètres de déploiement et les conventions de nommage.

Il est distribué exclusivement depuis son dépôt Git et installé avec **pipx**.

## Objectifs et principes

Lab Toolkit centralise les vérifications communes aux laboratoires, sans recopier de scripts dans chaque dépôt.

- **Un outil commun, indépendant** des dépôts qui l'utilisent : les configurations propres à chaque projet restent dans leur dépôt.
- **Cohérence et conventions** : contrôler les paramètres de déploiement et appliquer des conventions communes aux dépôts (voir les [évolutions](docs/evolution/)).
- **Initialisation** des fichiers de configuration nécessaires.
- **Vérifier, visualiser, appliquer** : trois étapes distinctes ; les modifications sont proposées avant d'être appliquées, jamais en silence.
- **Résultats reproductibles** en local et en CI.
- **Interface CLI homogène**, avec des retours d'exécution structurés.
- **Architecture modulaire**, reposant sur des dépendances réutilisables.
- **CD indépendant** : la phase de déploiement n'utilise pas Lab Toolkit.

## Contexte d'utilisation

| Environnement    | Utilisation                                                                             |
|------------------|-----------------------------------------------------------------------------------------|
| Poste de travail | Installation permanente avec pipx et gestion des configurations.                        |
| pre-commit       | Vérification de la configuration avant un commit.                                       |
| CI               | Installation temporaire et vérification automatisée.                                    |
| CD               | Installation temporaire et vérification automatisée et récupération des configurations. |

## Installation

Prérequis : Python 3.14 ou supérieur, Git et [pipx](https://pipx.pypa.io/).

Installer directement depuis le dépôt Git :
```bash
pipx install git+https://github.com/amine-guissouma/lab-toolkit.git
```

Cette commande installe le dernier état de la branche principale. Pour figer une version, notamment en CI :

```bash
pipx install git+https://github.com/amine-guissouma/lab-toolkit.git@<sha-ou-tag>
```

Vérifier l'installation :

```bash
lab-toolkit --version
```

> L'accès au dépôt Git est nécessaire pour installer ou mettre à jour Lab Toolkit. Aucune publication sur un registre Python n'est prévue.

## Utilisation
```bash
lab-toolkit deployment <commande> [--display-simple | --display-pipeline | --display-tree]
```

| Commande       | Rôle                                                                                                  |
|----------------|-------------------------------------------------------------------------------------------------------|
| `init`         | Crée `deployment.json` et `deployment_expected.json` s'ils n'existent pas (depuis la branche `socle`) |
| `validate`     | Vérifie que `deployment.json` correspond à la branche courante et et récupére les configurations.     |
| `show_config`  | Affiche la configuration actuelle et la configuration proposée                                        |
| `apply_config` | Écrit la configuration calculée dans `deployment.json`                                                |

### Modes d'affichage

Les commandes prennent en charge trois modes d'affichage :

| Option               | Description                             | Usage            |
|----------------------|-----------------------------------------|------------------|
| `--display-simple`   | Affichage synthétique du résultat.      | CI et pre-commit |
| `--display-pipeline` | Affichage chronologique des opérations. | diagnostic       |
| `--display-tree`     | Affichage hiérarchique des appels.      | diagnostic       |

Le mode `simple` est utilisé par défaut.


### Codes de sortie

- `0` : opération réussie.
- `1` : erreur de configuration, de branche Git ou d'exécution.

## Configuration

`deployment_expected.json` contient le répertoire racine de déploiement :

```json
{ "expectedRemoteDir": "/var/www/labs/mon-laboratoire" }
```

`deployment.json` contient la destination calculée pour la branche courante :

```json
{ "remoteDir": "/var/www/labs/mon-laboratoire/socle", "base": "/" }
```

| Branche            | `remoteDir`                             | `base`                |
|--------------------|-----------------------------------------|-----------------------|
| `socle`            | `<expectedRemoteDir>/socle`             | `/`                   |
| `experience/<nom>` | `<expectedRemoteDir>/experiences/<nom>` | `/experiences/<nom>/` |


## Intégration

Hook pre-commit :

```yaml
- repo: local
  hooks:
    - id: lab-toolkit-deployment-validation
      name: Lab Toolkit - Deployment validation
      entry: lab-toolkit deployment validate
      language: system
      pass_filenames: false
      always_run: true
```

Étape de CI (GitHub Actions) :

```yaml
- name: Installer lab-toolkit
  run: pipx install git+https://github.com/amine-guissouma/lab-toolkit@<sha>

- name: Valider la configuration de déploiement
  run: lab-toolkit deployment validate
```

## Développement

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check . && ruff format --check .
pre-commit install
```

## Architecture

Lab Toolkit distingue deux niveaux :

- **Core** : composants génériques de l'interface CLI, réutilisables indépendamment de l'application.
- **Application** : commandes et fonctionnalités propres à Lab Toolkit.

La journalisation et le suivi des opérations sont destinés à être fournis par une dépendance externe dédiée. Cette séparation permet de conserver un outil modulaire et de réutiliser le système de journalisation dans d'autres projets.

## Documentation

- [Architecture](docs/architecture.md)
- [Commandes](docs/commands.md)
- [Développement](docs/development.md)
- [Cycle d'utilisation](docs/deployment-workflow.md)
- [Évolutions envisagées](docs/evolution/)


## Évolutions envisagées

Des évolutions pourront être étudiées progressivement en fonction des besoins rencontrés dans les laboratoires.

Elles sont documentées dans [`docs/evolution/`](docs/evolution/).

# Statut
Version 0.1.0 en cours de développement (WIP). La première version sera publiée à la fin les deux premiers socles, frontend(v0.1.0) et backend(v0.1.0).

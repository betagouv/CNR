# CNR

L'application web qui soutient le projet du Conseil National de la Refondation (CNR).

## Prérequis

- Python 3.9
- Postgreql 13.x.

## Installer les pre-commit hooks

```
pre-commit install
```

On peut faire un premier test en faisant tourner :

```
pre-commit run --all-files
```

## Installation

Le projet peut se lancer en local ou avec Docker.

### En local

#### Créer un environnement virtuel

```
# Configurer et activer l'environnement virtuel
python -m venv venv
. venv/bin/activate

# Installer les packages requis
pip install -r requirements.txt
```

#### Copier les variables d'environnement

```
cp .env.example .env
```

#### Lancer le serveur

```
python manage.py runserver
```

#### Lancer les migrations

```
python manage.py migrate
```

#### Effectuer les tests

D'abord installer les dépendances de test :

```sh
pip install -r requirements_for_test.txt
```

Tests unitaires :

```
python manage.py test
```

Tests E2E :

Si vous n'utilisez pas Docker, il vous faudra `firefox` et
`geckodriver` accessibles sur votre machine pour lancer les tests
E2E. Sur macOS ils sont disponibles via `brew`.

```
make test-e2e
```


### via Docker

#### Copier les variables d'environnement

```sh
cp .env.example .env
```

#### Lancer les containers

```sh
docker-compose up
```

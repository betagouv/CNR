# CNR

`git clone https://github.com/betagouv/CNR.git`

# Installation local 
## Créer un environnement virtuel

```
# Configurer et activer l'environnement virtuel
python -m venv venv
. venv/bin/activate

# Installer les packages requis
pip install -r requirements.txt

# Copier les variables d'environnement
cp .env.example .env
```

## Lancer le serveur

```
python manage.py runserver
```

## Lancer les migrations

```
python manage.py migrate
```

## Effectuer les tests

```
python manage.py test
```

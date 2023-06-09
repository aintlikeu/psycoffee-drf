The project and README are in progress

## Quickstart
To get started with this project, clone the repository:
```
git clone https://github.com/aintlikeu/psycoffee-drf.git
```

Use poetry for installation
```
cd psycoffee-drf
poetry install      # install dependencies and create virtual environment
poetry shell        # activate virtual environment
```

Create config file. Fill in the file:
```
cd core
cp config.example.yaml config.yaml
```

Make and apply the database migrations:
```
python manage.py makemigrations
python manage.py migrate
```

Seed data:
```
python manage.py seed
```

Run the development server:
```
python manage.py runserver
```

The project will be available at http://127.0.0.1:8000/.

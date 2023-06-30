The project and README are in progress

## Current endpoints

```
api/spots
    POST api/spots
        request format:
        {
            "customer_id": <int>,
            "date": <int unixtimestamp>,
            "time": <"HH:MM">,   # (e.g. "11:00")
            "duration": <int>    # (from a list 60, 90, 120)
        }
        
    GET api/spots
    GET api/spots?customer_id={customer_id}&date={unixtimestamp}
    GET api/spots?customer_id={customer_id}&date={unixtimestamp}&whole_month=true
    
    DELETE api/spots
        request format:
        # delete specific spot
        {
            "customer_id": <int>,
            "date": <int unixtimestamp>,
            "time": <"HH:MM">,   # (e.g. "11:00")
        }
        # delete all spots on that day
        {
            "customer_id": <int>,
            "date": <int unixtimestamp>,
        }
        
api/bookings
    POST api/bookings
        request format:
        {
            "spot_id": <int>,
            "duration": <int>,    # (from a list 60, 90, 120, must be <= spot duration),
            "phone": <str>,       # "+7xxxxxxxxxx" format
            "name": <str>,
            "comment": <optional str>
        }
        
    GET api/bookings
    GET api/bookings?customer_id=<customer_id>&date=<unixtimestamp>
    GET api/bookings?customer_id=<customer_id>&date=<unixtimestamp>&whole_month=true
    
    DELETE api/bookings
        request format:
        {
            "customer_id": <int>,
            "date": <int unixtimestamp>,
            "time": <"HH:MM">,   # (e.g. "11:00")
        }
        
api/free_spots
    GET api/free_spots
    GET api/free_spots?customer_id={customer_id}&date={unixtimestamp}
    GET api/free_spots?customer_id={customer_id}&date={unixtimestamp}&whole_month=true

api/signup_user
    POST api/signup_user
        request format:
            {
                "phone": <str>,       # "+7xxxxxxxxxx" format,
                "password": <str>,
                "password2": <str>
            {

api/login_user
    POST api/login_user 
        request format:
            {
                "phone": <str>,       # "+7xxxxxxxxxx" format,
                "password": <str>
            }
            
api/logout_user
    GET api/logout_user
    
api/profile
    GET api/profile    
    
/auth/
    ^auth/ ^authorize/?$ [name='authorize']
    ^auth/ ^token/?$ [name='token']
    ^auth/ login/<str:backend>/ [name='begin']
    ^auth/ complete/<str:backend>/ [name='complete']
    ^auth/ disconnect/<str:backend>/ [name='disconnect']
    ^auth/ disconnect/<str:backend>/<int:association_id>/ [name='disconnect_individual']
    ^auth/ ^convert-token/?$ [name='convert_token']
    ^auth/ ^revoke-token/?$ [name='revoke_token']
    ^auth/ ^invalidate-sessions/?$ [name='invalidate_sessions']
    ^auth/ ^invalidate-refresh-tokens/?$ [name='invalidate_refresh_tokens']
    ^auth/ ^disconnect-backend/?$ [name='disconnect_backend']
```

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

## Set up Redis:
For other operating systems, use the official instructions https://redis.io/docs/getting-started/installation/
```
# for MacOS
brew install redis
redis-server                # to run in foreground
brew services start redis   # to run as service
brew services stop redis    # to stop service
```

## Run the development server:
```
python manage.py runserver
```

The project will be available at http://127.0.0.1:8000/.

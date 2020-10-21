# To run Development server using Docker

## To build the docker image

```
docker-compose build
```

## To run the docker image
```
docker-compose run
```

### To run Development server without using Docker

## Install the requirements
```
pip install -r requirements.txt
```

## To run the server
```
python manage.py runserver
```

# API
## Signup
```
POST - /user/
BODY - 
{
    "username": <username>,
    "password": <password>    
}
```
## Login
```
POST - /login/
BODY -
{
    "username": <username>,
    "password": <password>    
}
```
## Google Login
```
POST - /google_login/
BODY -
{
    "token": <token>
}
```


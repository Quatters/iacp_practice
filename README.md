# IACP Website demo

## Run locally in docker

1. Copy file `.example.env` to the root directory and
rename it to `.env`.
   
2. Provide next settings in this file:
   
    1. `SECRET_KEY` - any long string, preferably
    generated uuid/guid.
       
    2. `DJANGO_SU_USERNAME`, `DJANGO_SU_PASSWORD` -
    any credentials you want to use to enter the admin page.
    May stay defaults (admin/admin).
       
3. Build and up containers:

```shell
docker-compose build
docker-compose up
```

App can be reached at 80 port, e.g. 
[http://localhost](http://localhost).

Admin page can be reached at `/admin`, e.g
[http://locahost/admin](http://localhost/admin).

## Run dev-server locally
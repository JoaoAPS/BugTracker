# Bugtracker

An application that aids a team to keep track of bugs on the code of different projects.

## Instalation

### Dependencies
- [Docker](https://www.docker.com/get-started)
- [Docker-compose](https://docs.docker.com/compose/install/)


### Instructions
1. Clone the repository.
2. `cd` into the repo directory and run on your cli `docker-compose build`.
3. Run `docker-compose up` whenever you want to run the app. It will be available on [localhost:8000](http://localhost:8000).

This will run the developer version.
To run the production version, run `docker-compose -f docker-compose-prod.yml up`.
Note that you first have to create a `.env` and `.db.env` files on `docker/prod/` with the enviroment variables.
They are similar to those in `docker/dev/.env` and `docker/dev/.db.env`, but should also include a ALLOWED_HOSTS variable.

A default admin user is registered when the application is first built, use it to register other members.
```
email: admin@mail.com
password: admin
```

Remeber to change admin credentials on django admin (found on the [/admin url](http://localhost:8000/admin/)) afterward.

# Bugtracker

An application that aids a team to keep track of bugs on the code of different projects.

## Usage

1. Register the members of your team.
2. Create projects and add the designated members to them.
3. The team members can report bugs on the project.
4. Project supervisors can assign bugs to members to solve.
5. Assigned members can let others know when they're working on the bug and when it is fixed.

## Instalation

### Dependencies
- [Docker](https://www.docker.com/get-started)
- [Docker-compose](https://docs.docker.com/compose/install/)


### Instructions
1. Clone the repository
2. `cd` into the repo directory and run on your cli `docker-compose build`
3. Run `docker-compose up` whenever you want to run the app. It will be available on [localhost:8000].

This will run the developer version.
To run the production version, run `docker-compose -f docker-compose-prod.yml up`.
Note that you first have to create a `.env` and `.db.env` files on `docker/prod/` with the enviroment variables.
They are similar to those in `docker/prod/.env` and `docker/prod/.db.env`, but should also include a ALLOWED_HOSTS variable.

A default admin user is registers when the application is first built, use it to register other members.
```
email: admin@mail.com
password: admin
```

Remeber to change admin credentials on django admin (found on the [/admin url](http://localhost:8000/admin/)) afterward.
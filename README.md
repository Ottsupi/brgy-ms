# Barangay Management System

## Tech Stack

-   Django 5.2
-   Tailwind 4.1
-   Postgres 17
-   Gunicorn 23
-   Nginx
-   Docker

## How to run (dev)

0. Setup `.env` from the template `.env.sample`
1. Run `./release.dev.sh`
2. In VS Code with Dev Containers extension, open command palette and type "Reopen in Container"
3. Run `make run` to start the dev server
4. Open browser to `localhost:8000`

## How to run (local deployment)

0. Setup `.env` from the template `.env.sample`
1. Run `./release.local.sh`
2. Open browser to `localhost`

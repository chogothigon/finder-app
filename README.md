# CarFinder App

## Structure
- frontend/ — Vue.js frontend
- backend/ — Node.js + Express API
- backend/db — MySQL schema and seed data

## Software Used
- MySQL Server 8.x
- MySQL Workbench (optional GUI)
- Node.js + npm
- Express + mysql2
- Vue.js
- Git + GitHub

## Database Setup (MySQL)
1. Install MySQL Server on at least one team member machine.
2. Create a database (example):
	- `CREATE DATABASE finder_app;`
3. Configure backend environment variables:
	- `DB_HOST`
	- `DB_PORT` (default `3306`)
	- `DB_USER`
	- `DB_PASS`
	- `DB_NAME`

## Run Schema + Data Migrations
Use numbered files in `backend/db/migrations` in this order:
1. `001_create_schema.sql` (creates tables/constraints/indexes)
2. `002_seed_insert.sql` (dummy data insert migration)
3. `003_seed_delete.sql` (dummy data delete/depopulate migration)

Example with MySQL CLI:
- `mysql -u <user> -p <database> < backend/db/migrations/001_create_schema.sql`
- `mysql -u <user> -p <database> < backend/db/migrations/002_seed_insert.sql`

To depopulate:
- `mysql -u <user> -p <database> < backend/db/migrations/003_seed_delete.sql`

## Local Development
1. Install backend dependencies in `backend/`.
2. Run schema migration `001_create_schema.sql`.
3. Run insert migration `002_seed_insert.sql`.
4. Start backend API.
5. Start frontend.

## GitHub Milestone Checklist
- Create/use a shared GitHub repository.
- Add all team members as collaborators.
- Have each member commit at least one change.
- Store schema and migration SQL files in repo as backup.
- Do not commit secrets (passwords, tokens, private connection strings).

## Final Report Notes to Include
- GitHub repository URL and collaborator list.
- Evidence each teammate made a commit.
- MySQL version and tools used.
- Steps to connect to DB and run migrations.
- Any business-rule constraints implemented (PK, FK, CHECK, UNIQUE).


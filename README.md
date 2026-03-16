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
4. `004_create_views.sql` (REST API support views for final application pages)

Example with MySQL CLI:
- `mysql -u <user> -p <database> < backend/db/migrations/001_create_schema.sql`
- `mysql -u <user> -p <database> < backend/db/migrations/002_seed_insert.sql`
- `mysql -u <user> -p <database> < backend/db/migrations/004_create_views.sql`

To depopulate:
- `mysql -u <user> -p <database> < backend/db/migrations/003_seed_delete.sql`

## REST API Data Requirements by Page
Final page list: `search`, `user favorites`, `random car`, `car info + images`, `login`.

- `Search` page:
	- Endpoint: `GET /api/search/results`
	- Source view: `vw_search_results`
	- Data needed: `car_id`, `car_year`, `car_make`, `car_model`, `car_display_name`, `car_arrival_date`, `car_engine_data`, `car_active`, `car_source`, `primary_image_url`, `junkyard_id`, `junkyard_city`, `junkyard_state`, `junkyard_zip`, `junkyard_phone`, `junkyard_website`
	- Endpoint: `GET /api/search/filters`
	- Source view: `vw_search_filter_options`
	- Data needed: `car_make`, `car_model`, `car_year`, `junkyard_city`, `junkyard_state`

- `User Favorites` page (with sign-in data):
	- Endpoint: `GET /api/favorites/:userId`
	- Source view: `vw_user_favorites`
	- Data needed: `user_id`, `user_email`, `user_googleid`, plus favorited car/junkyard card data

- `Random Car` page:
	- Endpoint: `GET /api/random-car`
	- Source view: `vw_random_car_pool`
	- Data needed: same fields as search results for one random active car
	- Query pattern: `SELECT * FROM vw_random_car_pool ORDER BY RAND() LIMIT 1`

- `Car Info + Images` page:
	- Endpoint: `GET /api/cars/:carId`
	- Source view: `vw_car_info`
	- Data needed: full car detail, junkyard detail, `primary_image_url`, `image_count`, `favorite_count`
	- Endpoint: `GET /api/cars/:carId/images`
	- Source view: `vw_car_images`
	- Data needed: all image rows for a car (`image_id`, `car_id`, `image_url`)

- `Login` page:
	- Endpoint: `GET /api/login/users`
	- Source view: `vw_login_users`
	- Data needed: `user_id`, `user_email`, `user_googleid`

## Local Development
1. Install backend dependencies in `backend/`.
2. Run schema migration `001_create_schema.sql`.
3. Run insert migration `002_seed_insert.sql`.
4. Run views migration `004_create_views.sql`.
5. Start backend API.
6. Start frontend.

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


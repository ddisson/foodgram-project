# Foodgram

Foodgram is a web-based platform designed for food enthusiasts. Here, users can share, explore, and discover new recipes, making it the perfect platform for culinary adventures.

Main link http://158.160.76.30/

## 🍔 Features

- **Share Recipes**: Share your unique recipes with the community.
- **Discover & Explore**: Navigate through various categories and discover new recipes.
- **User Profiles**: Create and customize your profile. Save your favorite recipes and more!
- **Search**: Search for specific recipes or ingredients.
- **Rate & Comment**: Rate recipes and leave comments for feedback.

## 🛠 Prerequisites

- Python (>= 3.6)
- Docker
- Git

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ddisson/foodgram.git
cd foodgram

### 2. Setup the Virtual Environment

python -m venv venv
source venv/bin/activate

### 3. Install the Dependencies

pip install -r requirements.txt

### 4. Setup Environment Variables

Creta a .env file in root directory

SECRET_KEY='django-insecure-tty(dm80q($gnsb@z0d)j@a2#5$t=+2wp@z-0y@+jj%n)#ay0!'

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '158.160.76.30']

LANGUAGE_CODE=ru-ru 


### 5. Launch with Docker Compose
Use commnatd in terminal to builld containers

cd backend
docker build -t ddisson/foodgram_backend:latest .

cd frontend
docker build -t ddisson/foodgram_frontend:latest .

cd infra

docker-compose build
docker-compose up

Visit http://localhost:8000 to access the application.

### 6. Database Migrations
Run migrations to initialize the database:

docker-compose exec -T backend python manage.py makemigrations
docker-compose exec -T backend python manage.py migrate

## 7. Copy static and ingredients
docker-compose exec -T backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py import_ingredients /data/ingredients.csv

### 8. Create a Superuser
For accessing the admin panel:

docker-compose run --rm web python manage.py createsuperuser

Then, navigate to http://localhost:8000/admin and log in with the ssuperuser credentials and create Tags



📜 License
This project is licensed under the MIT License. See LICENSE.md for more details.

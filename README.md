
## Local setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements/development.txt

cp .env.example .env   # then fill in DJANGO_SECRET_KEY at minimum

python manage.py migrate
python manage.py createsuperuser

npm install
npm run build:css      # or: npm run watch:css while developing

python manage.py runserver
```

Visit `/` for the site and `/admin/` for the admin panel.

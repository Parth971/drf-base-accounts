Python version: 3.10.6

Step 1: Installing requirements:
cmd: pip install -r requirements.txt

Step 2: .env config:
Create .env file and enter configs.
```env
SETTINGS_MODULE_NAME=dev
```

Ref. : see sample_env.txt

Step 3: Run migrations
cdm: python manage.py makemigrations
cmd: python manage.py migrate

Step 4: To development runserver:
python manage.py runserver
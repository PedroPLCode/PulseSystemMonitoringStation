# PulseSystemMonitoringStation

PulseSystemMonitoringStation is an automated system monitoring bot that keeps track of your machine's status. It sends Telegram and/or email notifications if the CPU temperature exceeds 75°C. Designed for reliability, automation, and peace of mind.

## Features
- Real-time monitoring of system status (CPU temperature).
- Sends alerts via Telegram or email when critical thresholds are exceeded.
- Built-in Flask Admin Panel for user management and control.
- Easy configuration via .env file.
- xtendable with scheduled jobs, logging, and backups.

## Installation

To install and set up the bot locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PulseSystemMonitoringStation.git
cd PulseSystemMonitoringStation
```

2. Set up a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate or . venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment variables by creating a .env file with your Binance API credentials, database URL, and email, telegram configuration.
```bash
APP_SECRET_KEY = 'your_turbo_secret_key'
CSRF_SECRET_KEY = 'your_total_secret_key'
GMAIL_USERNAME = 'gmail@username.com'
GMAIL_APP_PASSWORD="gmail_app_password"
TELEGRAM_API_SECRET="telegram_api_secret_key"
RECAPTCHA_PUBLIC_KEY = "recaptcha_public_key"
RECAPTCHA_PRIVATE_KEY = "recaptcha_private_key"
etc
```

5. Set up the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run tests:
```bash
pytest
```

7. Run the Flask application:
```bash
flask run -h 0.0.0.0 -p 8000
```
or
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

8. Tweak, pimp, improve and have fun.

## Usage
Once running, the bot will automatically start monitoring CPU temperature and perform scheduled tasks such as:
- Resource monitoring (every minute)
- Log backup and email reports (every 24 hours)
- Database backups (every 24 hours)
The admin panel will be available under /admin.

## Technologies Used
- **Python**: The primary language used for development.
- **Flask**: A web framework used for building the application interface.
- **Flask-SQLAlchemy**: ORM used to manage the database.
- **Flask-JWT-Extended**: JWT-based authentication for securing user access.
- **Flask-Mail**: For sending email reports.
- **Python-Telegram-Bot**: For sending telegram trade informations.

## Important! 
Familiarize yourself thoroughly with the source code. Understand its operation. Only then will you be able to customize and adjust scripts to your own needs, preferences, and requirements. Only then will you be able to use it correctly and avoid potential issues. Knowledge of the underlying code is essential for making informed decisions and ensuring the successful implementation of the bot for your specific use case. Make sure to review all components and dependencies before running the scripts.

Code created by me, with no small contribution from Dr. Google and Mr. ChatGPT.
Any comments welcome.

PulseSystemMonitoringStation Project is under GNU General Public License Version 3, 29 June 2007
from flask import Flask, render_template, jsonify, redirect, url_for, flash, session
from apscheduler.schedulers.background import BackgroundScheduler
import os
import csv
import psutil
import requests
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import Config
from models import db, User, SystemMonitoringData, AdminModelView
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

admin = Admin(app, name='Pulse Monitoring Admin', template_mode='bootstrap4', base_template='admin/base.html')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(SystemMonitoringData, db.session))
#from models.admin import add_menu_links
#add_menu_links(admin)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # sprawdzenie czy to pierwszy użytkownik
            is_first_user = User.query.first() is None

            user = User(
                username=form.username.data,
                email=form.email.data,
                is_admin=is_first_user  # pierwszy user jest adminem
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            flash('Rejestracja zakończona sukcesem, możesz się teraz zalogować.', 'success')
            return redirect(url_for('login'))

        except IntegrityError:
            db.session.rollback()
            flash('Użytkownik o takim loginie lub adresie e-mail już istnieje.', 'danger')

        except Exception as e:
            db.session.rollback()
            flash(f'Wystąpił nieoczekiwany błąd: {str(e)}', 'danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            session.permanent = True
            current_user.update_last_login()
            return redirect(url_for('admin.index'))
        flash('Nieprawidłowy username lub hasło.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



def write_to_db(data):
    timestamp, cpu, ram, disk, net_sent, net_recv, cpu_temp = data

    # Tworzymy obiekt do zapisania
    record = SystemMonitoringData(
        timestamp=timestamp,
        cpu=cpu,
        ram=ram,
        disk=disk,
        net_sent=net_sent,
        net_recv=net_recv,
        cpu_temp=cpu_temp
    )

    # Dodajemy rekord do bazy danych
    db.session.add(record)
    db.session.commit()
    
    print('write_to_db()')


def check_services():
    services = ["nginx", "docker"]
    status = {}
    for service in services:
        result = os.system(f"systemctl is-active --quiet {service}")
        status[service] = "✅ OK" if result == 0 else "❌ Nie działa"
    return status

def check_resources():
    with app.app_context():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()
        net_sent = net.bytes_sent / (1024 * 1024)
        net_recv = net.bytes_recv / (1024 * 1024)
        temperature = psutil.sensors_temperatures()

        cpu_temp = None
        if "coretemp" in temperature:
            cpu_temp_data = temperature["coretemp"]
            if cpu_temp_data:
                cpu_temp = cpu_temp_data[0].current

        if cpu_temp is None:
            cpu_temp = "Brak danych"
            
        timestamp = datetime.now()
        data = [timestamp, cpu, ram, disk, net_sent, net_recv, cpu_temp]
        
        # Zapisz dane do bazy danych
        write_to_db(data)

        # Usuwanie danych starszych niż 24 godziny
        remove_old_data()

        print('check_resources()')
        
        #from utils.telegram_utils import filter_users_and_send_alert_telegram
        #filter_users_and_send_alert_telegram('test wyslany')
        
        #from utils.email_utils import filter_users_and_send_alert_email
        #filter_users_and_send_alert_email('test', 'ete sdsdf sdf dsf dsfdsfdsf ')

        return cpu, ram, disk, net_sent, net_recv, cpu_temp


def remove_old_data():
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    records_to_remove = SystemMonitoringData.query.filter(SystemMonitoringData.timestamp < cutoff_time).all()
    for record in records_to_remove:
        db.session.delete(record)
    db.session.commit()



@app.route("/api/data")
def get_data():
    data = SystemMonitoringData.query.order_by(SystemMonitoringData.timestamp).all()

    timestamps = [record.timestamp.isoformat() for record in data]
    cpu_usage = [record.cpu for record in data]
    ram = [record.ram for record in data]
    disk = [record.disk for record in data]
    net_sent = [record.net_sent for record in data]
    net_recv = [record.net_recv for record in data]
    temperature = [record.cpu_temp for record in data]

    return jsonify({
        "timestamps": timestamps,
        "cpu_usage": cpu_usage,
        "ram": ram,
        "disk": disk,
        "net_sent": net_sent,
        "net_recv": net_recv,
        "temperature": temperature
    })



@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Uruchomienie schedulera
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_resources, trigger="interval", minutes=1)  # Zbieranie danych co minutę
    scheduler.start()
    print('scheduler.start()')

start_scheduler()

# Funkcja tworzenia bazy danych
def create_db():
    with app.app_context():
        db.create_all()

# Uruchomienie aplikacji i scheduler
if __name__ == '__main__':
    create_db()  # Tworzymy tabele w bazie danych

    #if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    #    start_scheduler()  # Uruchamiamy scheduler tylko w głównym procesie

    app.run(debug=True, host='0.0.0.0', port=8000, use_reloader=True)

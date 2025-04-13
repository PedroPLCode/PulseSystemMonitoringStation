import os
import psutil
from datetime import datetime, timedelta
from models import db, Monitor
from app import app
from utils.logging import logger


def check_resources():
    with app.app_context():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
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

        write_to_db(data)

        remove_old_data()

        logger.info("check_resources()")

        if cpu_temp >= 85:
            sent_user_alert("cpu_temp >= 85", "cpu_temp >= 85")

        return cpu, ram, disk, net_sent, net_recv, cpu_temp


def sent_user_alert(title, msg):
    from utils.telegram_utils import filter_users_and_send_alert_telegram
    from utils.email_utils import filter_users_and_send_alert_email

    filter_users_and_send_alert_telegram(msg)
    filter_users_and_send_alert_email(title, msg)


def write_to_db(data):
    timestamp, cpu, ram, disk, net_sent, net_recv, cpu_temp = data

    record = Monitor(
        timestamp=timestamp,
        cpu=cpu,
        ram=ram,
        disk=disk,
        net_sent=net_sent,
        net_recv=net_recv,
        cpu_temp=cpu_temp,
    )

    db.session.add(record)
    db.session.commit()

    logger.info("write_to_db()")


def remove_old_data():
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    records_to_remove = Monitor.query.filter(Monitor.timestamp < cutoff_time).all()
    for record in records_to_remove:
        db.session.delete(record)
    db.session.commit()

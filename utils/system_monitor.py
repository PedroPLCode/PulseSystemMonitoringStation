import psutil
from datetime import datetime, timedelta
from typing import List, Tuple, Union
from models import db, Monitor
from app import app
from utils.logging import logger


def check_resources() -> Tuple[float, float, float, float, float, Union[float, str]]:
    """
    Checks the current system resource usage, stores it in the database, 
    removes outdated records, and sends alerts if necessary.

    Returns:
        Tuple containing:
        - CPU usage percentage (float)
        - RAM usage percentage (float)
        - Disk usage percentage (float)
        - Network bytes sent (in MB) (float)
        - Network bytes received (in MB) (float)
        - CPU temperature (float or 'Brak danych' if unavailable)
    """
    with app.app_context():
        cpu: float = psutil.cpu_percent()
        ram: float = psutil.virtual_memory().percent
        disk: float = psutil.disk_usage("/").percent
        net = psutil.net_io_counters()
        net_sent: float = net.bytes_sent / (1024 * 1024)
        net_recv: float = net.bytes_recv / (1024 * 1024)
        temperature = psutil.sensors_temperatures()

        cpu_temp: Union[float, str] = "Brak danych"
        if "coretemp" in temperature:
            cpu_temp_data = temperature["coretemp"]
            if cpu_temp_data:
                cpu_temp = cpu_temp_data[0].current

        timestamp: datetime = datetime.now()
        data: List[Union[datetime, float, str]] = [
            timestamp, cpu, ram, disk, net_sent, net_recv, cpu_temp
        ]

        write_to_db(data)
        remove_old_data()

        logger.info("check_resources() loop completed.")

        if isinstance(cpu_temp, float) and cpu_temp >= 75:
            now = datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            logger.warning(f"cpu_temp >= {cpu_temp}")
            alert_subject = "CPU Temperature Alert."
            alert_content = f"PulseSystemMonitoringStation\nhttps://pulse.ropeaccess.pro\n\nCPU temparature Alert.\n{formatted_now}\n\nCurrent cpu_temp >= {cpu_temp}"
            sent_user_alert(alert_subject, alert_content)

        return cpu, ram, disk, net_sent, net_recv, cpu_temp


def sent_user_alert(title: str, msg: str) -> None:
    """
    Sends a system alert to all configured users via Telegram and email.

    Args:
        title (str): The alert title for email.
        msg (str): The alert message content.
    """
    from utils.telegram_utils import filter_users_and_send_alert_telegram
    from utils.email_utils import filter_users_and_send_alert_email

    filter_users_and_send_alert_telegram(msg)
    filter_users_and_send_alert_email(title, msg)


def write_to_db(data: List[Union[datetime, float, str]]) -> None:
    """
    Writes a new resource monitoring record to the database.

    Args:
        data (List): A list containing:
            - timestamp (datetime)
            - CPU usage percentage (float)
            - RAM usage percentage (float)
            - Disk usage percentage (float)
            - Network sent (MB) (float)
            - Network received (MB) (float)
            - CPU temperature (float or str)
    """
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

    logger.info("write_to_db() New data written to database")


def remove_old_data() -> None:
    """
    Removes monitoring records older than 24 hours from the database.
    """
    cutoff_time: datetime = datetime.utcnow() - timedelta(hours=24)
    records_to_remove = Monitor.query.filter(Monitor.timestamp < cutoff_time).all()
    for record in records_to_remove:
        db.session.delete(record)
    db.session.commit()
    logger.info("remove_old_data() Data older than 24 hours removed from database.")

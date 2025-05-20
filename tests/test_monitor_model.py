from datetime import datetime
from app.models import db
from app.models import Monitor


def test_create_monitor_entry(app):
    with app.app_context():
        timestamp = datetime(2024, 10, 10, 12, 0, 0)
        monitor = Monitor(
            timestamp=timestamp,
            cpu=23.5,
            ram=45.0,
            disk=67.8,
            net_sent=12.34,
            net_recv=56.78,
            cpu_temp=55.1,
        )

        db.session.add(monitor)
        db.session.commit()

        assert monitor.id is not None
        assert monitor.timestamp == timestamp
        assert monitor.cpu == 23.5
        assert monitor.ram == 45.0
        assert monitor.disk == 67.8
        assert monitor.net_sent == 12.34
        assert monitor.net_recv == 56.78
        assert monitor.cpu_temp == 55.1
        assert f"<Monitor {timestamp}>" == repr(monitor)


def test_monitor_default_timestamp(app):
    with app.app_context():
        monitor = Monitor(
            cpu=10.0, ram=20.0, disk=30.0, net_sent=1.0, net_recv=2.0, cpu_temp=40.0
        )

        db.session.add(monitor)
        db.session.commit()

        assert monitor.timestamp is not None
        assert isinstance(monitor.timestamp, datetime)
        assert f"<Monitor {monitor.timestamp}>" == repr(monitor)

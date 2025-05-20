import json
from datetime import datetime
from app.models import Monitor, Settings
from app import db


def test_get_data_success(client, app):
    with app.app_context():
        db.session.query(Monitor).delete()
        db.session.query(Settings).delete()

        settings = Settings(cpu_alert_temp=80.0)
        db.session.add(settings)

        monitor_entry = Monitor(
            timestamp=datetime(2024, 1, 1, 12, 0),
            cpu=25.5,
            ram=50.1,
            disk=30.2,
            net_sent=10.0,
            net_recv=15.5,
            cpu_temp=65.0,
        )
        db.session.add(monitor_entry)
        db.session.commit()

    response = client.get("/api/data")

    assert response.status_code == 200
    data = json.loads(response.data)

    assert data["timestamps"] == ["2024-01-01T12:00:00"]
    assert data["cpu_usage"] == [25.5]
    assert data["ram"] == [50.1]
    assert data["disk"] == [30.2]
    assert data["net_sent"] == [10.0]
    assert data["net_recv"] == [15.5]
    assert data["temperature"] == [65.0]
    assert data["temperature_limit"] == 80.0


def test_get_data_no_settings(client, app):
    with app.app_context():
        db.session.query(Monitor).delete()
        db.session.query(Settings).delete()

        db.session.commit()

    response = client.get("/api/data")
    assert response.status_code == 500
    assert b"error" in response.data

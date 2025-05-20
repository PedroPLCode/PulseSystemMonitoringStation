from app.models import Monitor, Settings
from datetime import datetime


def test_dashboard_view(client, app):
    with app.app_context():
        settings = Settings(cpu_alert_temp=80.0)
        Monitor.query.delete()
        Settings.query.delete()
        settings = Settings(cpu_alert_temp=80.0)
        app.db.session.add(settings)

        last_monitor = Monitor(
            timestamp=datetime.utcnow(),
            cpu=10.0,
            ram=20.0,
            disk=30.0,
            net_sent=40.0,
            net_recv=50.0,
            cpu_temp=60.0,
        )
        app.db.session.add(last_monitor)
        app.db.session.commit()

    response = client.get("/")
    assert response.status_code == 200
    assert b"dashboard" in response.data or b"Dashboard" in response.data

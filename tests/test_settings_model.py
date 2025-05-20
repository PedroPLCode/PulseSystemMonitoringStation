from app.models import db
from app.models import Settings


def test_create_settings_with_defaults(app):
    with app.app_context():
        settings = Settings()
        db.session.add(settings)
        db.session.commit()

        assert settings.id is not None
        assert settings.cpu_alert_temp == 75
        assert settings.alerts_frequency_hrs == 1
        assert "<Limit id=" in repr(settings)


def test_create_settings_with_custom_values(app):
    with app.app_context():
        settings = Settings(cpu_alert_temp=85.5, alerts_frequency_hrs=2.5)
        db.session.add(settings)
        db.session.commit()

        assert settings.cpu_alert_temp == 85.5
        assert settings.alerts_frequency_hrs == 2.5
        assert f"<Limit id={settings.id}, cpu_alert_temp=85.5>" == repr(settings)

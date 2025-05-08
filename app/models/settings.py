from app.models import db


class Settings(db.Model):
    """
    Represents threshold Settings for various system metrics, such as CPU temperature.
    Used to store configuration values for system monitoring.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    cpu_alert_temp: float = db.Column(db.Float, default=75, nullable=False)
    alerts_frequency_hrs: float = db.Column(db.Float, default=1, nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Settings object, primarily for debugging.
        """
        return f"<Limit id={self.id}, cpu_alert_temp={self.cpu_alert_temp}>"

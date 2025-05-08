from app.models import db


class Limits(db.Model):
    """
    Represents threshold limits for various system metrics, such as CPU temperature.
    Used to store configuration values for system monitoring.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    cpu_temp: float = db.Column(db.Float, default=75, nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Limits object, primarily for debugging.
        """
        return f"<Limit id={self.id}, cpu_temp={self.cpu_temp}>"

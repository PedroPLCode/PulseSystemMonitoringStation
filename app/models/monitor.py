from datetime import datetime
from typing import Optional
from models import db


class Monitor(db.Model):
    """
    A database model representing system resource usage at a specific point in time.

    Attributes:
        id (int): The unique identifier of the record.
        timestamp (datetime): The time when the data was recorded.
        cpu (float): The CPU usage percentage.
        ram (float): The RAM usage percentage.
        disk (float): The disk usage percentage.
        net_sent (float): The amount of data sent over the network (in MB).
        net_recv (float): The amount of data received over the network (in MB).
        cpu_temp (Optional[str]): The CPU temperature in degrees Celsius as a string (can be None).
    """

    id: int = db.Column(db.Integer, primary_key=True)
    timestamp: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cpu: float = db.Column(db.Float, nullable=False)
    ram: float = db.Column(db.Float, nullable=False)
    disk: float = db.Column(db.Float, nullable=False)
    net_sent: float = db.Column(db.Float, nullable=False)
    net_recv: float = db.Column(db.Float, nullable=False)
    cpu_temp: Optional[str] = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Monitor record.

        Returns:
            str: A string containing the timestamp of the record.
        """
        return f"<Monitor {self.timestamp}>"

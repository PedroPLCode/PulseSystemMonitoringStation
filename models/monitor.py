from datetime import datetime
from models import db

class SystemMonitoringData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cpu = db.Column(db.Float, nullable=False)
    ram = db.Column(db.Float, nullable=False)
    disk = db.Column(db.Float, nullable=False)
    net_sent = db.Column(db.Float, nullable=False)
    net_recv = db.Column(db.Float, nullable=False)
    cpu_temp = db.Column(db.String(50), nullable=True)  # Może być None, jeśli brak danych o temperaturze

    def __repr__(self):
        return f"<SystemMonitoringData {self.timestamp}>"

from flask import jsonify
from models import Monitor
from app import app
from utils.exception_handler import exception_handler


@exception_handler()
@app.route("/api/data")
def get_data():
    data = Monitor.query.order_by(Monitor.timestamp).all()

    timestamps = [record.timestamp.isoformat() for record in data]
    cpu_usage = [record.cpu for record in data]
    ram = [record.ram for record in data]
    disk = [record.disk for record in data]
    net_sent = [record.net_sent for record in data]
    net_recv = [record.net_recv for record in data]
    temperature = [record.cpu_temp for record in data]

    return jsonify(
        {
            "timestamps": timestamps,
            "cpu_usage": cpu_usage,
            "ram": ram,
            "disk": disk,
            "net_sent": net_sent,
            "net_recv": net_recv,
            "temperature": temperature,
        }
    )

from flask import jsonify, Response
from app.models import Monitor, Limits
from app import app
from app.utils.exception_handler import exception_handler
from typing import Any


@exception_handler()
@app.route("/api/data")
def get_data() -> Response:
    """
    API endpoint to fetch monitoring data from the database.

    Retrieves all monitor records, ordered by timestamp, and returns them
    as a JSON response containing the following fields:
        - timestamps (list of str)
        - cpu_usage (list of float)
        - ram (list of float)
        - disk (list of float)
        - net_sent (list of float)
        - net_recv (list of float)
        - temperature (list of str or None)

    Returns:
        Response: A Flask JSON response with monitoring data or an error message.
    """
    try:
        limits = Limits.query.order_by(Limits.timestamp.desc()).first()
        data: list[Monitor] = Monitor.query.order_by(Monitor.timestamp).all()

        timestamps: list[str] = [record.timestamp.isoformat() for record in data]
        cpu_usage: list[float] = [record.cpu for record in data]
        ram: list[float] = [record.ram for record in data]
        disk: list[float] = [record.disk for record in data]
        net_sent: list[float] = [record.net_sent for record in data]
        net_recv: list[float] = [record.net_recv for record in data]
        temperature: list[Any] = [record.cpu_temp for record in data]
        temperature_limit: float = limits.cpu_temp

        return jsonify(
            {
                "timestamps": timestamps,
                "cpu_usage": cpu_usage,
                "ram": ram,
                "disk": disk,
                "net_sent": net_sent,
                "net_recv": net_recv,
                "temperature": temperature,
                "temperature_limit": temperature_limit,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

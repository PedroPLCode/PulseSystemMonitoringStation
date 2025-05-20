import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from app.utils.system_monitor import check_resources
from app.models import Monitor, Settings


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@patch("app.utils.check_resources.psutil.cpu_percent", return_value=30.5)
@patch("app.utils.check_resources.psutil.virtual_memory")
@patch("app.utils.check_resources.psutil.disk_usage")
@patch("app.utils.check_resources.psutil.net_io_counters")
@patch("app.utils.check_resources.psutil.sensors_temperatures")
@patch("app.utils.check_resources.write_to_db")
@patch("app.utils.check_resources.remove_old_data")
@patch("app.utils.check_resources.Settings")
@patch("app.utils.check_resources.logger")
@patch("app.utils.check_resources.sent_user_alert")
def test_check_resources_normal_flow(
    mock_alert,
    mock_logger,
    mock_settings,
    mock_remove_old_data,
    mock_write_to_db,
    mock_sensors,
    mock_net_io,
    mock_disk_usage,
    mock_virtual_memory,
    mock_cpu_percent,
    app_context,
):
    mock_virtual_memory.return_value.percent = 40.1
    mock_disk_usage.return_value.percent = 50.2
    mock_net_io.return_value.bytes_sent = 1024 * 1024 * 10  # 10 MB
    mock_net_io.return_value.bytes_recv = 1024 * 1024 * 20  # 20 MB

    mock_sensors.return_value = {"coretemp": [MagicMock(current=75.0)]}

    mock_settings.query.first.return_value = MagicMock(cpu_alert_temp=70)

    result = check_resources.check_resources()

    cpu, ram, disk, net_sent, net_recv, cpu_temp = result

    assert cpu == 30.5
    assert ram == 40.1
    assert disk == 50.2
    assert abs(net_sent - 10.0) < 0.01
    assert abs(net_recv - 20.0) < 0.01
    assert cpu_temp == 75.0

    mock_write_to_db.assert_called_once()
    mock_remove_old_data.assert_called_once()
    mock_logger.info.assert_called_with("check_resources() loop completed.")

    mock_alert.assert_called_once()


@patch("app.utils.check_resources.psutil.sensors_temperatures")
@patch("app.utils.check_resources.Settings")
@patch("app.utils.check_resources.sent_user_alert")
@patch("app.utils.check_resources.write_to_db")
@patch("app.utils.check_resources.remove_old_data")
@patch("app.utils.check_resources.logger")
def test_check_resources_no_cpu_temp(
    mock_logger,
    mock_remove_old_data,
    mock_write_to_db,
    mock_sent_user_alert,
    mock_settings,
    mock_sensors,
    app_context,
):
    mock_sensors.return_value = {}

    mock_settings.query.first.return_value = MagicMock(cpu_alert_temp=70)

    with patch("app.utils.check_resources.psutil.cpu_percent", return_value=10), patch(
        "app.utils.check_resources.psutil.virtual_memory"
    ) as vm, patch("app.utils.check_resources.psutil.disk_usage") as du, patch(
        "app.utils.check_resources.psutil.net_io_counters"
    ) as net_io:

        vm.return_value.percent = 20
        du.return_value.percent = 30
        net_io.return_value.bytes_sent = 0
        net_io.return_value.bytes_recv = 0

        result = check_resources.check_resources()

    cpu, ram, disk, net_sent, net_recv, cpu_temp = result

    assert cpu_temp == "Brak danych"

    mock_sent_user_alert.assert_not_called()

    mock_write_to_db.assert_called_once()
    mock_remove_old_data.assert_called_once()
    mock_logger.info.assert_called_with("check_resources() loop completed.")


@patch("app.utils.check_resources.db")
@patch("app.utils.check_resources.Monitor")
@patch("app.utils.check_resources.logger")
def test_write_to_db(mock_logger, mock_monitor_class, mock_db, app_context):
    data = [datetime(2025, 5, 20, 12, 0), 10.1, 20.2, 30.3, 1.1, 2.2, 50.0]

    instance = MagicMock()
    mock_monitor_class.return_value = instance

    check_resources.write_to_db(data)

    mock_monitor_class.assert_called_once_with(
        timestamp=data[0],
        cpu=data[1],
        ram=data[2],
        disk=data[3],
        net_sent=data[4],
        net_recv=data[5],
        cpu_temp=data[6],
    )
    mock_db.session.add.assert_called_once_with(instance)
    mock_db.session.commit.assert_called_once()
    mock_logger.info.assert_called_with("write_to_db() New data written to database")


@patch("app.utils.check_resources.Monitor")
@patch("app.utils.check_resources.db")
@patch("app.utils.check_resources.logger")
def test_remove_old_data(mock_logger, mock_db, mock_monitor_class, app_context):
    cutoff = datetime.now() - timedelta(hours=24)
    old_record = MagicMock()
    mock_monitor_class.query.filter.return_value.all.return_value = [old_record]

    check_resources.remove_old_data()

    mock_monitor_class.query.filter.assert_called()
    mock_db.session.delete.assert_called_once_with(old_record)
    mock_db.session.commit.assert_called_once()
    mock_logger.info.assert_called_with(
        "remove_old_data() Data older than 24 hours removed from database."
    )

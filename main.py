import sys
from traffic_monitor.traffic_monitor_app import TrafficMonitorAPP

if __name__ == '__main__':
    app = TrafficMonitorAPP()
    sys.exit(app.exec_())

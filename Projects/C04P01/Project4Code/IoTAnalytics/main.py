import time
from pathlib import Path

import IoTAnalytics
from IoTAnalytics.Config.core import DATASET_DIR, PROCESS_DIR, config
from Database import Aggregation



while True:
    try:

       # Aggregate Data For Device 1
        Aggregation.aggregate_heart_rate_data(config.app_config.deviceid1)

        # Aggregate Data For Device 2
        Aggregation.aggregate_heart_rate_data(config.app_config.deviceid2)

        time.sleep(config.app_config.Anomaly_Time_Check_Interval)

    #Disconnect the client from MQTT broker and stop the loop gracefully at
    # Keyboard interrupt (Ctrl+C)
    except KeyboardInterrupt:

        break






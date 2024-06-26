CREATE OR REPLACE STREAM "ANOMALY_DATA_STREAM"
(
    deviceid VARCHAR(32),
    COL_timestamp TIMESTAMP,
    datatype VARCHAR(16),
    COL_value DECIMAL
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS
INSERT INTO "ANOMALY_DATA_STREAM"
    SELECT STREAM "deviceid", "COL_timestamp", "datatype", "COL_value" FROM "SOURCE_SQL_STREAM_001"
	WHERE "datatype" = 'HeartRate' AND "COL_value" NOT BETWEEN 65 AND 90;

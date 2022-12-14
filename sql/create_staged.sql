CREATE TABLE IF NOT EXISTS pskreporter_staged (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    snr INT,
    comm_mode TEXT,
    frequency DOUBLE PRECISION,
    rxtime_utc TIMESTAMPTZ,
    sender_callsign TEXT,
    sender_locator TEXT,
    sender_lat REAL,
    sender_lon REAL,
    receiver_callsign TEXT,
    receiver_locator TEXT,
    receiver_lat REAL,
    receiver_lon REAL,
    distance_mi REAL,
    insertion_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT staged_psk_prim_key PRIMARY KEY (rxtime_utc, sender_callsign, receiver_callsign),
    CONSTRAINT staged_check_kc1qby CHECK (receiver_callsign LIKE '%KC1QBY%' OR sender_callsign LIKE '%KC1QBY%')
);

CREATE TABLE IF NOT EXISTS logbook_staged (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    qso_date DATE,
    time_off TEXT,
    frequency DOUBLE PRECISION,
    comm_mode TEXT,
    receiver_callsign TEXT,
    receiver_locator TEXT,
    receiver_lat REAL,
    receiver_lon REAL,
    sender_callsign TEXT,
    sender_locator TEXT,
    sender_lat REAL,
    sender_lon REAL,
    distance_mi REAL,
    rst_rcvd INTEGER,
    rst_sent INTEGER,
    tx_pwr INTEGER,
    app_qrzlog_logid BIGINT,
    qrzcom_qso_upload_date DATE,
    insertion_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT staged_log_prim_key PRIMARY KEY (app_qrzlog_logid)
);

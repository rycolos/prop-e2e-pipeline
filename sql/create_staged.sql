CREATE TABLE pskreporter_staged (
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
    insert_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT staged_prim_key PRIMARY KEY (rxtime_utc, sender_callsign, receiver_callsign),
    CONSTRAINT staged_check_kc1qby CHECK (receiver_callsign LIKE '%KC1QBY%' OR sender_callsign LIKE '%KC1QBY%')
)

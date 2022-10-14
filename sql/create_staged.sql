CREATE TABLE pskreporter_staged (
    sNR INT,
    commMode TEXT,
    frequency DOUBLE PRECISION,
    rxTime TEXT,
    senderCallsign TEXT,
    senderLocator TEXT,
    senderLat REAL,
    senderLon REAL,
    receiverCallsign TEXT,
    receiverLocator TEXT,
    receiverLat REAL,
    receiverLon REAL,
	CONSTRAINT staged_prim_key PRIMARY KEY (rxTime, senderCallsign, receiverCallsign),
	CONSTRAINT staged_check_kc1qby CHECK (receiverCallsign LIKE '%KC1QBY%' OR senderCallsign LIKE '%KC1QBY%')
)

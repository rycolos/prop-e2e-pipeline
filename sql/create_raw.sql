CREATE TABLE pskreporter_raw (
    sNR TEXT NOT NULL,
    mode TEXT,
    MHz TEXT NOT NULL,
    rxTime TEXT NOT NULL,
    senderDXCC TEXT,
    flowStartSeconds TEXT,
    senderCallsign TEXT NOT NULL,
    senderLocator TEXT NOT NULL,
    receiverCallsign TEXT NOT NULL,
    receiverLocator TEXT NOT NULL,
    receiverAntennaInformation TEXT,
    senderDXCCADIF TEXT,
    submode TEXT,
	CONSTRAINT raw_prim_key PRIMARY KEY (rxTime, senderCallsign, receiverCallsign),
	CONSTRAINT raw_check_kc1qby CHECK (receiverCallsign LIKE '%KC1QBY%' OR senderCallsign LIKE '%KC1QBY%')
)
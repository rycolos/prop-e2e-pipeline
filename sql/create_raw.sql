CREATE TABLE pskreporter_raw (
    id INTEGER GENERATED ALWAYS AS IDENTITY,
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
	CONSTRAINT comp_key PRIMARY KEY (rxTIME, senderCallsign, receiverCallsign),
	CONSTRAINT check_kc1qby CHECK (receiverCallsign LIKE '%KC1QBY%' OR senderCallsign LIKE '%KC1QBY%')
)
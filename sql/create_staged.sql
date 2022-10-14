-- CREATE TABLE pskreporter_staged AS 
-- 	SELECT
-- 		CAST(sNR AS INTEGER),
-- 		mode AS commMode,
-- 		CAST(MHz AS DOUBLE PRECISION) AS frequency,
-- 		senderCallsign,
-- 		senderLocator,
-- 		receiverCallsign,
-- 		receiverLocator
-- 	FROM pskreporter_raw;

-- ALTER TABLE pskreporter_staged ADD COLUMN id INTEGER GENERATED ALWAYS AS IDENTITY;
-- ALTER TABLE pskreporter_staged ADD COLUMN senderLat REAL;
-- ALTER TABLE pskreporter_staged ADD COLUMN senderLon REAL;
-- ALTER TABLE pskreporter_staged ADD COLUMN receiverLat REAL;
-- ALTER TABLE pskreporter_staged ADD COLUMN receiverLon REAL;

CREATE TABLE pskreporter_staged (
    id INTEGER GENERATED ALWAYS AS IDENTIY,
    sNR INTEGER,
    commMode TEXT,
    frequency DOUBLE PRECISION,
    senderCallsign TEXT,
    senderLocator TEXT,
    senderLat REAL,
    senderLon REAL,
    receiverCallsign TEXT,
    receiverLocator TEXT,
    receiverLat REAL,
    receiverLon REAL
	CONSTRAINT comp_key PRIMARY KEY (rxTIME, senderCallsign, receiverCallsign),
	CONSTRAINT check_kc1qby CHECK (receiverCallsign LIKE '%KC1QBY%' OR senderCallsign LIKE '%KC1QBY%')
)

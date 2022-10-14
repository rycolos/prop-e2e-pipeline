CREATE TABLE pskreporter_staged AS 
	SELECT
		CAST(sNR AS INTEGER),
		mode AS commMode,
		CAST(MHz AS DOUBLE PRECISION) AS frequency,
		senderCallsign,
		senderLocator,
		receiverCallsign,
		receiverLocator
	FROM pskreporter_raw;

ALTER TABLE pskreporter_staged ADD COLUMN id INTEGER GENERATED ALWAYS AS IDENTITY;
ALTER TABLE pskreporter_staged ADD COLUMN senderLat REAL;
ALTER TABLE pskreporter_staged ADD COLUMN senderLon REAL;
ALTER TABLE pskreporter_staged ADD COLUMN receiverLat REAL;
ALTER TABLE pskreporter_staged ADD COLUMN receiverLon REAL;
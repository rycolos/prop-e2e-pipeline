CREATE TABLE pskreporter_staged AS 
	SELECT
		CAST(sNR AS INTEGER),
		mode AS commMode,
		CAST(MHz AS DOUBLE PRECISION) AS frequency,
		senderCallsign,
		senderLocator,
		CAST(NULL AS REAL) AS senderLat,
		CAST(NULL AS REAL) AS senderLon,
		receiverCallsign,
		receiverLocator,
		CAST(NULL AS REAL) AS receiverLat,
		CAST(NULL AS REAL) AS receiverLon
	FROM pskreporter_raw;

ALTER TABLE pskreporter_staged ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY
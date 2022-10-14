INSERT INTO pskreporter_staged (sNR, commMode, frequency, senderCallsign, senderLocator, receiverCallsign, receiverLocator)
SELECT 
    CAST(sNR AS INT),
    mode,
    CAST(MHz AS DOUBLE PRECISION),
    senderCallsign,
    senderLocator,
    receiverCallsign,
    receiverLocator
FROM pskreporter_raw
ON CONFLICT DO NOTHING;
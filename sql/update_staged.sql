INSERT INTO pskreporter_staged (sNR, commMode, frequency, rxTime_utc, senderCallsign, senderLocator, receiverCallsign, receiverLocator)
SELECT
    CAST(sNR AS INT),
    mode,
    CAST(MHz AS DOUBLE PRECISION),
    TO_TIMESTAMP(rxtime, 'YYYY-MM-DD HH24:MI:SS') AT TIME ZONE 'UTC',
    senderCallsign,
    senderLocator,
    receiverCallsign,
    receiverLocator
FROM pskreporter_raw
ON CONFLICT DO NOTHING;
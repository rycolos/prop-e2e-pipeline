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

UPDATE pskreporter_staged
SET distance_mi = CAST(SQRT(POW(69.1 * (senderlat -  receiverlat), 2) + POW(69.1 * (receiverlon - senderlon) * COS(senderlat / 57.3), 2)) AS REAL)
WHERE distance_mi IS NULL;
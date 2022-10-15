UPDATE pskreporter_staged
SET distance_mi = CAST(SQRT(POW(69.1 * (senderlat -  receiverlat), 2) + POW(69.1 * (receiverlon - senderlon) * COS(senderlat / 57.3), 2)) AS REAL)
WHERE distance_mi IS NULL;
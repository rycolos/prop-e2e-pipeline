INSERT INTO pskreporter_staged (sNR, commMode, frequency, senderCallsign, senderLocator, receiverCallsign, receiverLocator)
SELECT sNR, mode, MHz, senderCallsign, senderLocator, receiverCallsign, receiverLocator
FROM pskreporter_raw;
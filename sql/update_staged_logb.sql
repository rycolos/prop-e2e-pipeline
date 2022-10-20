INSERT INTO logbook_staged (qso_date, time_off, frequency, comm_mode, receiver_callsign, receiver_locator, sender_callsign, sender_locator, rst_rcvd, rst_sent, tx_pwr, app_qrzlog_logid, qrzcom_qso_upload_date)
SELECT
    qso_date,
    time_off,
    frequency,
    mode,
    call,
    gridsquare,
    station_callsign,
    my_gridsquare,
    rst_rcvd,
    rst_sent,
    tx_pwr,
    app_qrzlog_logid,
    qrzcom_qso_upload_date
FROM logbook_raw
ON CONFLICT DO NOTHING;
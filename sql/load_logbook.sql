CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT 
	app_qrzlog_logid, 
	call, 
	frequency, 
	country, 
	gridsquare, 
	mode, 
	my_country, 
	my_gridquare, 
	qrzcom_qso_upload_date, 
	qso_date, 
	rst_rcvd, 
	rst_sent, 
	station_callsign, 
	time_off, 
	tx_pwr 
FROM logbook_raw; 
COPY tmp_table 
FROM '/home/kepler/prop-e2e-pipeline/adif_parser/adi-test.csv' 
WITH (FORMAT CSV, HEADER, DELIMITER ','); 

INSERT INTO pskreporter_raw (
	app_qrzlog_logid, 
	call, 
	frequency, 
	country, 
	gridsquare, 
	mode, 
	my_country, 
	my_gridsquare, 
	qrzcom_qso_upload_date, 
	qso_date, 
	rst_rcvd, 
	rst_sent, 
	station_callsign, 
	time_off, 
	tx_pwr 
)
SELECT
	app_qrzlog_logid, 
	call, 
	frequency, 
	country, 
	gridsquare, 
	mode, 
	my_country, 
	my_gridsquare, 
	qrzcom_qso_upload_date, 
	qso_date, 
	rst_rcvd, 
	rst_sent, 
	station_callsign, 
	time_off, 
	tx_pwr 
FROM tmp_table
ON CONFLICT DO NOTHING;
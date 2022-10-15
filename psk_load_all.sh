#!/bin/bash

DOCKERDATADIR="/var/lib/postgresql/data/psk_data"
DB="prop-e2e"
USER="postgres"

#APPEND TO RAW DB
echo "Appending to DB..."
docker exec -i prop-e2e-pipeline-postgres-1 cat $DOCKERDATADIR/*_psk.csv | psql -d $DB -U $USER --command="CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
COPY tmp_table \
FROM stdin \
WITH (FORMAT CSV, HEADER, DELIMITER ','); \
INSERT INTO pskreporter_raw \
SELECT * FROM tmp_table \
ON CONFLICT DO NOTHING;"
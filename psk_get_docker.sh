#!/bin/bash

CALLSIGN="KC1QBY"
DATADIR="$(pwd)/postgres_data/psk_data"
DOCKERDATADIR="/var/lib/postgresql/data/psk_data"
DB="prop-e2e"
USER="postgres"

mkdir -p "$DATADIR"

#GET FILE
wget "https://pskreporter.info/cgi-bin/pskdata.pl?callsign=$CALLSIGN" -O "$DATADIR"/temp.zip
unzip -d "$DATADIR" "$DATADIR"/temp.zip
mv "$DATADIR"/psk_data.csv "$DATADIR"/$(date +%Y-%m-%d)_psk.csv
rm "$DATADIR"/temp.zip

#CLEAN WITH SED (remove extra double quotes from antennainfo field)
sed -i  's/\([^,]\)"\([^,]\)/\1\2/g' "$DATADIR"/$(date +%Y-%m-%d)_psk.csv

#APPEND TO DB
docker exec -i prop-e2e-pipeline-postgres-1 psql -d $DB -U $USER --command="CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
COPY tmp_table \
FROM '$DOCKERDATADIR/$(date +%Y-%m-%d)_psk.csv' \
WITH (FORMAT CSV, HEADER, DELIMITER ','); \
INSERT INTO pskreporter_raw \
SELECT * FROM tmp_table \
ON CONFLICT DO NOTHING;"
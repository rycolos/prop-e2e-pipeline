#!/bin/bash

CALLSIGN="KC1QBY"
DATADIR="$(pwd)/psk_data"
JOBDIR="$(pwd)/jobs"
DB="prop-e2e"
USER="postgres"

mkdir -p "$DATADIR"
mkdir -p "$JOBDIR"

#GET FILE
wget "https://pskreporter.info/cgi-bin/pskdata.pl?callsign=$CALLSIGN" -O "$DATADIR"/temp.zip
unzip -d "$DATADIR" "$DATADIR"/temp.zip
mv "$DATADIR"/psk_data.csv "$DATADIR"/$(date +%Y-%m-%d)_psk.csv
rm "$DATADIR"/temp.zip

#CLEAN WITH SED (remove extra double quotes from antennainfo field)
sed -i '' 's/\([^,]\)"\([^,]\)/\1\2/g' "$DATADIR"/$(date +%Y-%m-%d)_psk.csv

#APPEND TO DB
# psql -d $DB -U $USER --command="CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
# COPY tmp_table \
# FROM '$DATADIR/$(date +%Y-%m-%d)_psk.csv'\
# WITH (FORMAT CSV, HEADER, DELIMITER ','); \
# INSERT INTO pskreporter_raw \
# SELECT * FROM tmp_table \
# ON CONFLICT DO NOTHING;"

docker exec -i prop-e2e-pipeline-postgres-1 psql -d $DB -U $USER --command="CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
COPY tmp_table \
FROM '$DATADIR/$(date +%Y-%m-%d)_psk.csv'\
WITH (FORMAT CSV, HEADER, DELIMITER ','); \
INSERT INTO pskreporter_raw \
SELECT * FROM tmp_table \
ON CONFLICT DO NOTHING;"

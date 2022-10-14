DATADIR="$(pwd)/psk_data"
DB="prop-e2e"
USER="postgres"

docker exec -i prop-e2e-pipeline-postgres-1 psql -d $DB -U $USER --command="CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
COPY tmp_table \
FROM '/var/lib/postgresql/data/psk_data/$(date +%Y-%m-%d)_psk.csv' \
WITH (FORMAT CSV, HEADER, DELIMITER ','); \
INSERT INTO pskreporter_raw \
SELECT * FROM tmp_table \
ON CONFLICT DO NOTHING;"

# 
import os, psycopg2, re

CALLSIGN="KC1QBY"
DATADIR="/home/kepler/prop-e2e-pipeline/postgres_data/psk_data"
DOCKERDATADIR="/var/lib/postgresql/data/psk_data"
DB="prop-e2e"
USER="postgres"

unpruned_f = os.listdir(DATADIR)
pruned_f = []

#remove from list if not ending in .sh
for index, item in enumerate(unpruned_f):
    #print(f"{index} - {item}")
    if re.match('^.*\.csv$', item):
        pruned_f.append(item)

print(pruned_f)

conn = psycopg2.connect(database="prop-e2e", host="192.168.1.91", user="postgres", password="postgres", port="5432")
cur = conn.cursor()

for item in pruned_f:
    cmd = f'''
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
    COPY tmp_table \
    FROM '{DOCKERDATADIR}/{item}' \
    WITH (FORMAT CSV, HEADER, DELIMITER ','); \
    INSERT INTO pskreporter_raw \
    SELECT * FROM tmp_table \
    ON CONFLICT DO NOTHING;
    '''

    cur.execute(cmd)

    for i in cur.fetchall():
        print(i)
  
conn.commit()
conn.close()
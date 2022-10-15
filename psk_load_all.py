import os, psycopg2, re

DATADIR = '/home/kepler/prop-e2e-pipeline/postgres_data/psk_data'
DOCKERDATADIR = '/var/lib/postgresql/data/psk_data'
DB = 'prop-e2e'
USER = 'postgres'
PW = 'postgres'
HOST = '192.168.1.91'
PORT = '5432'

unpruned_f = os.listdir(DATADIR)
pruned_f = []

#remove from list if not ending in .sh
for index, item in enumerate(unpruned_f):
    if re.match('^.*\.csv$', item):
        pruned_f.append(item)

print(f"Uploading...\n{pruned_f}")

conn = psycopg2.connect(database=DB, host=HOST, user=USER, password=PW, port=PORT)
cur = conn.cursor()

for item in pruned_f:
    query = f'''
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM pskreporter_raw; \
    COPY tmp_table \
    FROM '{DOCKERDATADIR}/{item}' \
    WITH (FORMAT CSV, HEADER, DELIMITER ','); \
    INSERT INTO pskreporter_raw \
    SELECT * FROM tmp_table \
    ON CONFLICT DO NOTHING;
    '''

    cur.execute(query)
    conn.commit()

cur.close()
conn.close()
import os, psycopg2, re, sys, yaml

DATADIR = '/home/kepler/prop-e2e-pipeline/postgres_data/psk_data'
DOCKERDATADIR = '/var/lib/postgresql/data/psk_data'

script_dir = os.path.dirname(__file__)
config_path = f'{script_dir}/config.yaml'

def config_parse(config_path):
    #Parse yaml config file for db, user, pw, host, port
    try:
        with open(config_path, 'r') as file:
            config_file = yaml.safe_load(file)
    except FileNotFoundError as e:
        print(f'File {config_path} not found. Exiting.')
        sys.exit(1)
    try:
        db = config_file['database_info']['database']
        user = config_file['database_info']['username']
        pw = config_file['database_info']['password']
        host = config_file['database_info']['host']
        port = config_file['database_info']['port']
    except KeyError as e:
        print(f'Config missing key: {e}. Exiting.')
        sys.exit(1)
    return db, user, pw, host, port

unpruned_f = os.listdir(DATADIR)
pruned_f = []

#remove from list if not ending in .sh
for index, item in enumerate(unpruned_f):
    if re.match('^.*\.csv$', item):
        pruned_f.append(item)

print(f"Uploading...\n{pruned_f}")

db, user, pw, host, port = config_parse(config_path)

conn = psycopg2.connect(database=db, host=host, user=user, password=pw, port=port)
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
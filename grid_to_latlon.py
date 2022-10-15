import os, psycopg2, yaml

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

def to_location(grid):
    # takes grid string and returns top-left lat, lon of grid square
    # modified from https://github.com/space-physics/maidenhead
    
    grid = grid.strip().upper()

    N = len(grid)
    if not 8 >= N >= 2 and N % 2 == 0:
        raise ValueError("Maidenhead locator requires 2-8 characters, even number of characters")

    Oa = ord("A")
    lon = -180.0
    lat = -90.0
    # first pair - world
    lon += (ord(grid[0]) - Oa) * 20
    lat += (ord(grid[1]) - Oa) * 10
    # second pair - region
    if N >= 4:
        lon += int(grid[2]) * 2
        lat += int(grid[3]) * 1
     # third pair - metro
    if N >= 6:
        lon += (ord(grid[4]) - Oa) * 5.0 / 60
        lat += (ord(grid[5]) - Oa) * 2.5 / 60
    return lat, lon

db, user, pw, host, port = config_parse(config_path)

conn = psycopg2.connect(database=db, host=host, user=user, password=pw, port=port)
cur = conn.cursor()

cur.execute("SELECT id, senderLocator, senderLat, senderLon, receiverLocator, receiverLat, receiverLon FROM pskreporter_staged FOR UPDATE")
result = cur.fetchall()

print(f"Converting grid square to lat, lon...\n")
sendCount = 0
recvCount = 0

for row in result:
    if row[2] is None or row[3] is None:
        sender = row[1]
        sender = sender[0:6]
        
        try:
            senderLat, senderLon = to_location(sender)
        except Exception:
            continue
        
        #print(sender, senderLat, senderLon)
        
        cur.execute(f"UPDATE pskreporter_staged SET senderlat = {senderLat} WHERE id = {row[0]}")
        cur.execute(f"UPDATE pskreporter_staged SET senderlon = {senderLon} WHERE id = {row[0]}")
        conn.commit()
        sendCount += 1

    if row[5] is None or row[6] is None:
        receiver = row[4]
        receiver = receiver[0:6]
        
        try:
            receiverLat, receiverLon = to_location(receiver)
        except Exception:
            continue

        #print(receiver, receiverLat, receiverLon) 
        
        cur.execute(f"UPDATE pskreporter_staged SET receiverlat = {receiverLat} WHERE id = {row[0]}")
        cur.execute(f"UPDATE pskreporter_staged SET receiverlon = {receiverLon} WHERE id = {row[0]}")
        conn.commit()
        recvCount += 1

print(f"{sendCount} rows updated.")
print(f"{recvCount} rows updated.")

cur.close()
conn.close()

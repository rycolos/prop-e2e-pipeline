import psycopg2

def to_location(maiden):
    maiden = maiden.strip().upper()

    N = len(maiden)
    if not 8 >= N >= 2 and N % 2 == 0:
        raise ValueError("Maidenhead locator requires 2-8 characters, even number of characters")

    Oa = ord("A")
    lon = -180.0
    lat = -90.0
    # first pair
    lon += (ord(maiden[0]) - Oa) * 20
    lat += (ord(maiden[1]) - Oa) * 10
    # second pair
    if N >= 4:
        lon += int(maiden[2]) * 2
        lat += int(maiden[3]) * 1
    if N >= 6:
        lon += (ord(maiden[4]) - Oa) * 5.0 / 60
        lat += (ord(maiden[5]) - Oa) * 2.5 / 60
    if N >= 8:
        lon += int(maiden[6]) * 5.0 / 600
        lat += int(maiden[7]) * 2.5 / 600
    return lat, lon

conn = psycopg2.connect(database="prop-e2e",
                        host="192.168.1.91",
                        user="postgres",
                        password="postgres",
                        port="5432")

cur = conn.cursor()
cur.execute("SELECT id, senderLocator, senderLat, senderLon, receiverLocator, receiverLat, receiverLon FROM pskreporter_staged FOR UPDATE")
result = cur.fetchall()

for row in result:
    if row[2] is None or row[3] is None:
        sender = row[1]
        sender = sender[0:8]
        senderLat, senderLon = to_location(sender)
        print(sender, senderLat, senderLon)
        cur.execute(f"UPDATE pskreporter_staged SET senderlat = {senderLat} WHERE id = {row[0]}")
        cur.execute(f"UPDATE pskreporter_staged SET senderlon = {senderLon} WHERE id = {row[0]}")

    if row[5] is None or row[6] is None:
        receiver = row[4]
        receiver = receiver[0:8]
        receiverLat, receiverLon = to_location(receiver)
        print(receiver, receiverLat, receiverLon) 
        cur.execute(f"UPDATE pskreporter_staged SET receiverlat = {receiverLat} WHERE id = {row[0]}")
        cur.execute(f"UPDATE pskreporter_staged SET receiverlon = {receiverLon} WHERE id = {row[0]}")

    conn.commit()
    
cur.close()
conn.close()

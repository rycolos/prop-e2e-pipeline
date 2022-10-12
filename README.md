# prop-e2e-pipeline

Create cronjob - download psk data every Monday at 1AM

`(crontab -l ; echo "0 1 * * 1 sh home/user/prop_e2e_pipeline/psk_get.sh") | crontab -`

## Create Table
```
CREATE TABLE Test (
id SERIAL,
sNR TEXT,
mode TEXT,
frequency REAL,
rxTime TIMESTAMP,
senserDXCC TEXT,
senderCallsign TEXT,
senderGridTEXT,
senderLat REAL,
senderLon REAL,
receiverCallsign TEXT,
receiverGrid TEXT,
receiverLat REAL,
receiverLon REAL
)
```

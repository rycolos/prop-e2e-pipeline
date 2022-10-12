# prop-e2e-pipeline

Create cronjob - download psk data every 6 days at 1AM

`(crontab -l ; echo "0 1 */6 * * sh /home/USER/prop_e2e_pipeline/psk_get.sh") | crontab -`

## Create Table
```
CREATE TABLE psk-raw (
    sNR TEXT,
    mode TEXT,
    MHz REAL,
    rxTime TIMESTAMP,
    senserDXCC TEXT,
    flowStartSeconds BIGINT,
    senderCallsign TEXT,
    senderLocator TEXT,
    receiverCallsign TEXT,
    receiverLocator TEXT,
    receiverAntennaInformation TEXT,
    senderDXCCADIF INT,
    submode TEXT
)
```

```
CREATE TABLE psk-received (
    id SERIAL,
    sNR TEXT,
    mode TEXT,
    frequency REAL,
    rxTime TIMESTAMP,
    senserDXCC TEXT,
    senderCallsign TEXT,
    senderGrid TEXT,
    senderLat REAL,
    senderLon REAL,
    receiverCallsign TEXT,
    receiverGrid TEXT,
    receiverLat REAL,
    receiverLon REAL
)
```

```
CREATE TABLE psk-received_by (
    id SERIAL,
    sNR TEXT,
    mode TEXT,
    frequency REAL,
    rxTime TIMESTAMP,
    senserDXCC TEXT,
    senderCallsign TEXT,
    senderGrid TEXT,
    senderLat REAL,
    senderLon REAL,
    receiverCallsign TEXT,
    receiverGrid TEXT,
    receiverLat REAL,
    receiverLon REAL
)
```

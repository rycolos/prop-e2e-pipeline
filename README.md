# **prop-e2e-pipeline**

## Objective
As an amateur radio operator, I am frequently experimenting with antennas and new communication modes. I would like to begin quantifying these experiments to analyze how different variables affect my signal propagation. 

## High-level data flow
<img src="https://i.imgur.com/RBmN2Y7.png" width="800">

## Tooling
1. PostgreSQL
2. Docker, Docker Compose
3. Python 3
4. Grafana, Prometheus

## Setup
### Run `make all`
Runs all key tasks to build postgres container, create tabes and views, ingest initial dataset, and perform transformation.
1. `clean` - Stops docker compose (if running) and removes containers
2. `start` - Starts docker compose and brings up containers
3. `create-base-tables` - Creates initial `pskreporter_raw` and `pskreporter_staged` tables
4. `create-views` - Create analytics-ready views on `pskreporter_staged`
5. `add-data` - Loads existing data from `postgres_data/psk_data` folder into `pskreporter_raw`, transforms and inserts into `pskreporter_staged`, performs a function to convert grid square > lat/lon and inserts into `pskreporter_staged`, and performs a function to calculate station-to-station distance and inserts into `pskreporter_staged` 

Run `make all-no-load` to run all tasks except `add-data`

## Maintenance

Add tasks for the following to the root crontab:
1. Pull 7d data dump daily from pskreporter, perform basic cleaning, and append to `pskreporter_raw`
2. Perform a daily INSERT of `pskreporter_raw` into `pskreporter_staged`
3. Run a daily function to convert maidenhead grid square (`senderLocator` and `receiverLocator`) to lat/lon on `pskreporter_staged`
4. Run a daily function to calculate station-to-station distance on `pskreporter_staged`
```
0 4 * * *  printf "$(date)\n********************\n" >> /home/kepler/prop-e2e-pipeline/cronlog.log 2>&1
0 4 * * * sh /home/kepler/prop-e2e-pipeline/psk_get_docker.sh >> /home/kepler/prop-e2e-pipeline/cronlog.log 2>&1
30 4 * * * cat /home/kepler/prop-e2e-pipeline/sql/update_staged.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e >> /home/kepler/prop-e2e-pipeline/cronlog.log 2>&1
0 5 * * * python3 /home/kepler/prop-e2e-pipeline/grid_to_latlon.py >> /home/kepler/prop-e2e-pipeline/cronlog.log 2>&1
30 5 * * * cat /home/kepler/prop-e2e-pipeline/sql/latlon_to_distance.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e >> /home/kepler/prop-e2e-pipeline/cronlog.log 2>&1
```

## Tables

**pskreporter_raw**

Raw daily dump from https://pskreporter.info, filtered for my callsign (`KC1QBY`). Mild cleaning using `sed` is performed prior to ingestion to remove any interjected double-quotes from the free-text `receiverAntennaInformation` column.

**pskreporter_staged**

Pre-analysis table with data types updated, irrelevant columns removed, columns renamed for clarity, and an auto-incrementing `id` column added. Three derived data colums are added: (1) sender/receiver latitude and (2) sender/receiver longitude are populated via a daily python scripts that convert maidenhead grid locator to lat/lon and (3) station-to-station distance is populated via a daily sql script.

**received**

Filtered view on `pskreporter_staged` to only show signals received at my station.

**received_by**

Filtered view on `pskreporter_staged` to only show signals of mine that have been received by other stations.

## Example Analysis Queries

**Median signal-to-noise ratio**
```
SELECT PERCENTILE_CONT(.5) WITHIN GROUP(ORDER BY snr) FROM received
SELECT PERCENTILE_CONT(.5) WITHIN GROUP(ORDER BY snr) FROM received_by
```

**Mapping of received_by stations**
```
SELECT receiverLat as lat, receiverLon as lon FROM received_by
```
Visualized with plotly and pandas:
<img src="https://i.imgur.com/z8cbSwe.png">

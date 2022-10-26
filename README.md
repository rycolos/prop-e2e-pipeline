# **prop-e2e-pipeline**

## Objective
As an amateur radio operator, I am frequently experimenting with antennas and new communication modes. I would like to begin quantifying these experiments to analyze how different variables affect my signal propagation. This project serves a dual purpose of assisting in my continued learning about data and analytics engineering.

## High-level data flow
<img src="https://i.imgur.com/kf085sm.png" width="800">

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
3. `create-base-tables` - Creates initial `pskreporter` and `logbook` raw and staged tables.
4. `create-views` - Create analytics-ready views on staged tables.
5. `add-data` - Loads existing data from `postgres_data/source_data` folder into relevant raw tables. Transforms and inserts into staged tables.
6. `drop` - Delete all tables 

Run `make all-no-load` to run all tasks except `add-data`

## Maintenance
### Automated pskreporter data ingest and transformation
Add tasks for the following to the root crontab:
1. Pull 7d data dump daily from pskreporter, perform basic cleaning, and append to `pskreporter_raw`
2. Perform a daily INSERT of `pskreporter_raw` into `pskreporter_staged`
3. Run a daily function to convert maidenhead grid square (`sender_locator` and `receiver_locator`) to lat/lon on `pskreporter_staged`
4. Run a daily function to calculate station-to-station distance on `pskreporter_staged`

### Automated logbook data ingest and transformation
1. Pull 7d dump of logbook via qrz.com API, perform basic cleaning, and parse from .adi file to .csv (via `adif_parser_qrz.py`).
2. Append .csv to `logbook_raw` and insert non-duplicate `logbook_raw` records into `logbook_staged` (with `logb_get.sh`).

## Tables

**pskreporter_raw**

Raw daily dump from https://pskreporter.info, filtered for my callsign (`KC1QBY`). Mild cleaning using `sed` is performed prior to ingestion to remove any interjected double-quotes from the free-text `receiverAntennaInformation` column.

**pskreporter_staged**

Pre-analysis table with data types updated, irrelevant columns removed, columns renamed for clarity, and an auto-incrementing `id` column added. Three derived data colums are added: (1) sender/receiver latitude and (2) sender/receiver longitude are populated via a daily python scripts that convert maidenhead grid locator to lat/lon and (3) station-to-station distance is populated via a daily sql script.

**received**

Filtered view on `pskreporter_staged` to only show signals received at my station.

**received_by**

Filtered view on `pskreporter_staged` to only show signals of mine that have been received by other stations.

**logbook_raw**
Raw 7d dump from my qrz.com logbook, using their official logbook api: https://www.qrz.com/docs/logbook30/api. Mild cleaning using `sed` is performed prior to ingest to handle special characters. 

**logbook_staged**
Pre-analysis tables with column name changes and type casting for better analysis. 

## Example Analysis Queries

**Median signal-to-noise ratio**
```
SELECT PERCENTILE_CONT(.5) WITHIN GROUP(ORDER BY snr) FROM received
SELECT PERCENTILE_CONT(.5) WITHIN GROUP(ORDER BY snr) FROM received_by
```

**Mapping of received_by stations**
```
SELECT receiver_lat as lat, receiver_lon as lon FROM received_by
```
Visualized with plotly and pandas:
<img src="https://i.imgur.com/z8cbSwe.png">

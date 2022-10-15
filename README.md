# **prop-e2e-pipeline**

## PostgresSQL, Python, Docker Compose

### Setup

1. Run `docker compose up -d` to start the postgres container. Username, password, and database name are currently hardcoded in `docker-compose.yml`. 
2. Create `pskreporter_raw` DB via docker shell: `cat sql/create_raw.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
3. Create `pskreporter_staged` DB docker via docker shell: `cat sql/create_staged.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
4. Create analysis views - `create_view_received.sql` and `create_view_received_by.sql`

### Maintenance

1. Pull 7d data dump daily from pskreporter, perform basic cleaning, and append to `pskreporter_raw`
    1. Add the following to the root crontab: `0 8 * * * sh /home/kepler/prop_e2e_pipeline/psk_get_docker.sh`
2. Perform a daily INSERT of `pskreporter_raw` into `pskreporter_staged`
    1. Add the following to the root crontab: `0 9 * * * cat sql/udpated_staged.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
3. Run a daily function to convert maidenhead grid square (`senderLocator` and `receiverLocator`) to lat/lon on `pskreporter_staged`
    1. Add the following to the root crontab: `0 10 * * * python3 /home/kepler/prop_e2e_pipeline/grid_to_latlon.py`

### Tables

**pskreporter_raw**

Raw daily dump from https://pskreporter.info, filtered for my callsign (`KC1QBY`). Mild cleaning using `sed` is performed prior to ingestion to remove any interjected double-quotes from the free-text `receiverAntennaInformation` column.

**pskreporter_staged**

Pre-analysis table with data types updated, irrelevant columns removed, columns renamed for clarity, an auto-incrementing `id` column added, and lat/lon columns added for conversion from maidenhead grid columns (`senderLocator` and `receiverLocator`).

**received**

Filtered view on `pskreporter_staged` to only show signals received at my station.

**received_by**

Filtered view on `pskreporter_staged` to only show signals of mine that have been received by other stations.

# prop-e2e-pipeline

1. Run docker-compose.yml: `docker compose up -d`
2. Create `pskreporter_raw` DB in docker: `cat sql/create_raw.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
3. Create `pskreporter_staged` DB in docker: `cat sql/create_staged.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
4. Schedule daily get latest data + append to `pskreporter_raw`: `0 8 * * * sh /home/kepler/prop_e2e_pipeline/psk_get_docker.sh`
5. Copy daily `pskreporter_raw` to `pskreporter_staged` with `update_staged.sql`
6. Run `grid_to_latlon.py` on staged db to transform `senderLocator` and `receiverLocator` to lat/lon columns in `pskreporter_staged`
7. Create views - `create_view_received.sql` and `create_view_received_by.sql`. 

# prop-e2e-pipeline

## Docker
1. Run docker-compose.yml: `docker compose up -d`
2. Create DB in docker: `cat sql/create_raw.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
3. Schedule daily get + append tasks: `0 8 * * * sh /home/kepler/prop_e2e_pipeline/psk_get_docker.sh`
4. Run `grid_to_latlon.py` on staged db to transform `senderLocator` and `receiverLocator` to lat/lon columns

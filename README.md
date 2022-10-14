# prop-e2e-pipeline

## Docker
1. Run docker-compose.yml
2. Create DB in docker: `cat sql/create_raw.sql | docker exec -i prop-e2e-pipeline-postgres-1 psql -U postgres -d prop-e2e`
3. Schedule daily get + append tasks: `0 8 * * * sh /home/kepler/prop_e2e_pipeline/psk_get_docker.sh`

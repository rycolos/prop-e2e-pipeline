# prop-e2e-pipeline
Create cronjob - download psk data every 7 days
`(crontab -l ; echo "5 8 * * 7 sh home/user/prop_e2e_pipeline/psk_get.sh") | crontab -`

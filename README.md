# prop-e2e-pipeline

Create cronjob - download psk data every Monday at 1AM

`(crontab -l ; echo "0 1 * * 1 sh home/user/prop_e2e_pipeline/psk_get.sh") | crontab -`

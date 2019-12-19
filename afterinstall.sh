#!/usr/bin/env bash
cp /home/ec2-user/tokens.py /matryoshka/matryoshka/matryoshka/spiders/
cp /home/ec2-user/google_api_credentials.json /matryoshka/

touch /matryoshka/cron.log
sudo chmod 666 /matryoshka/cron.log
sudo chmod 777 /matryoshka/matryoshka_daily.sh

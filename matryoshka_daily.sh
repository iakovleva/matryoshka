#!/usr/bin/env bash
export SSH_AUTH_SOCK=/ssh-agent
/usr/local/bin/docker-compose -f /matryoshka/docker-compose.yml run -e SSH_AUTH_SOCK=/ssh-agent --rm app python3 matryoshka/matryoshka/spiders/leads.py
/usr/local/bin/docker-compose -f /matryoshka/docker-compose.yml run -e SSH_AUTH_SOCK=/ssh-agent --rm app python3 matryoshka/matryoshka/spiders/leads_dogovor.py
/usr/local/bin/docker-compose -f /matryoshka/docker-compose.yml run -e SSH_AUTH_SOCK=/ssh-agent --rm app python3 matryoshka/matryoshka/spiders/leads_nesnyatie.py
/usr/local/bin/docker-compose -f /matryoshka/docker-compose.yml run -e SSH_AUTH_SOCK=/ssh-agent --rm app python3 matryoshka/matreshka_data.py
sudo rm /matryoshka/leads.csv

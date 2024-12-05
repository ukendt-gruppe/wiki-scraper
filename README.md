# wiki-scraper
This repo politely scrapes wikipages

## Overview
This project is a Wikipedia scraper built using Scrapy, designed to politely and responsibly collect data from Wikipedia pages while respecting rate limits and robots.txt rules.

## Features
- Polite scraping with configurable delays and concurrent request limits
- PostgreSQL database integration for storing scraped data
- Environment variable configuration
- Logging and error handling

## Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Create Python Virtual Environment and Install Dependencies
```
python -m venv venv
LINUX/MAC: source venv/bin/activate
WINDOWS: source venv/Scripts/activate
pip install -r requirements.txt
```

### Setup Environment Variables
```
cp .env.example .env
Copy environment variables from to .env
```

### Migrate Database to local 
```
alembic head upgrade
```

### Run Database Locally
```
IN ONE TERMINAL WINDOW:
cd docker
docker compose -f docker-compose.dev.yml up

IN ANOTHER TERMINAL WINDOW:
docker exec -it <db_container_name> psql -U <db_user> -d <db_name>
```

### Run Database Deployed
```
ssh -v -i ~/.ssh/<key_name> <user>@<vm ip>
docker exec -it <db_container_name> psql -U <db_user> -d <db_name>

```

### Run Scraper and Save to Local PostgreSQL
```
cd wikicrawler
scrapy crawl wiki
```

### Backup Production Database
```
python scripts/backup_prod_db.py
```
### Migrate scraped data to PostgreSQL
```
PYTHONPATH=$PYTHONPATH:. python scripts/migrate_to_prod.py
```
### Restore Production Database From Latest Backup (WIP)
```
### Migrate Production Database To Local (WIP)
```

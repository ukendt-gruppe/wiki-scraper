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

### Setup Environment Variables
```
cp .env.example .env
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

### Run Scraper
```
cd wikicrawler
scrapy crawl wiki
```
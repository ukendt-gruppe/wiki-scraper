import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

def backup_production_db():
    load_dotenv()
    
    # Create backups directory if it doesn't exist
    if not os.path.exists('backups'):
        os.makedirs('backups')

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backups/prod_backup_{timestamp}.sql'

    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    # Parse database URL to get components
    parsed_url = urlparse(database_url)
    db_name = parsed_url.path.lstrip('/')  # Remove leading slash from path
    db_user = parsed_url.username
    db_pass = parsed_url.password
    db_host = parsed_url.hostname
    db_port = parsed_url.port

    # Execute pg_dump using Docker
    try:
        subprocess.run([
            'docker', 'run', '--rm',
            '-v', f'{os.getcwd()}/backups:/backups',
            '-e', f'PGPASSWORD={db_pass}',
            'postgres:latest',
            'pg_dump',
            '-h', db_host,
            '-p', str(db_port),
            '-U', db_user,
            '-d', db_name,
            '--no-owner',
            '--no-acl',
            '-f', f'/backups/prod_backup_{timestamp}.sql'
        ], check=True, stderr=subprocess.PIPE)
        print(f"Backup created successfully: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {str(e)}")
        print(f"Error output: {e.stderr.decode()}")

if __name__ == "__main__":
    backup_production_db()
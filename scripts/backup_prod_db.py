import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

def backup_production_db():
    load_dotenv()
    
    # Create backups directory if it doesn't exist
    if not os.path.exists('backups'):
        os.makedirs('backups')

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backups/prod_backup_{timestamp}.sql'

    # Get database URL from environment
    database_url = os.getenv('LOCAL_DATABASE_URL')
    
    # Parse database URL to get components
    # Assuming format: postgresql://user:password@host:port/dbname
    db_info = database_url.replace('postgresql://', '').split('/')
    db_name = db_info[1]
    db_user, db_pass = db_info[0].split('@')[0].split(':')
    db_host = db_info[0].split('@')[1].split(':')[0]
    
    # Set environment variables for pg_dump
    env = os.environ.copy()
    env['PGPASSWORD'] = db_pass

    # Execute pg_dump
    try:
        subprocess.run([
            'pg_dump',
            '-h', db_host,
            '-U', db_user,
            '-d', db_name,
            '-f', backup_file
        ], env=env, check=True)
        print(f"Backup created successfully: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {str(e)}")

if __name__ == "__main__":
    backup_production_db()
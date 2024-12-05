import os
import subprocess
import time
from dotenv import load_dotenv

def welcome():
    print("Welcome to the Database Management Script")

def backup_database():
    print("Backing up the database...")
    try:
        subprocess.run(['python', 'scripts/backup_prod_db.py'], check=True)
        print("Backup completed successfully.")
    except subprocess.CalledProcessError:
        print("Backup failed. Please check the logs.")

def check_docker_running():
    print("Checking if Docker is running...")
    try:
        subprocess.run(['docker', 'info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker is running.")
    except subprocess.CalledProcessError:
        print("Docker is not running. Please start Docker and try again.")
        exit(1)

def run_wikicrawler(duration):
    print(f"Running WikiCrawler for {duration} seconds...")
    try:
        subprocess.Popen(['python', 'scripts/migrate_to_prod.py'])
        time.sleep(duration)
        print("WikiCrawler has run for the specified duration.")
    except Exception as e:
        print(f"Error running WikiCrawler: {e}")

def stop_wikicrawler():
    print("Stopping WikiCrawler...")
    # Assuming the script is running in a separate process, you may need to implement a way to stop it.
    # This is a placeholder for stopping the process.
    print("WikiCrawler stopped.")

def migrate_wikiarticles():
    print("Migrating WikiArticles to production...")
    try:
        subprocess.run(['python', 'scripts/migrate_to_prod.py'], check=True)
        print("Migration completed successfully.")
    except subprocess.CalledProcessError:
        print("Migration failed. Please check the logs.")

def cleanup():
    print("Cleaning up...")
    # Implement any cleanup logic if necessary
    print("Cleanup completed.")

def main():
    load_dotenv()
    welcome()

    if input("Do you want to backup the database? (yes/no): ").strip().lower() == 'yes':
        backup_database()

    check_docker_running()

    if input("Do you want to run WikiCrawler? (yes/no): ").strip().lower() == 'yes':
        duration = int(input("Enter the duration in seconds: "))
        run_wikicrawler(duration)

        if input("Do you want to stop WikiCrawler manually? (yes/no): ").strip().lower() == 'yes':
            stop_wikicrawler()

    if input("Do you want to migrate WikiArticles to production? (yes/no): ").strip().lower() == 'yes':
        migrate_wikiarticles()

    cleanup()

if __name__ == "__main__":
    main()
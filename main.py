"""
Sales Report Automation - Main Entry Point
Supports dynamic theme switching based on config.json customized_theme setting
"""

from datetime import datetime
import json
from dotenv import load_dotenv
import logging
import schedule
import time
import os
from cryptography.fernet import Fernet
from io import StringIO
import pytz

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


from config import COUNTRY_CONFIG


def get_pkt_time(target_time_str, target_country):
    """Convert target country's local time to Pakistan Time (PKT) for scheduling"""
    try:
        country_info = COUNTRY_CONFIG.get(target_country, COUNTRY_CONFIG['PK'])
        target_tz = pytz.timezone(country_info['timezone'])
        pkt_tz = pytz.timezone('Asia/Karachi')
        
        now = datetime.now()
        # Create target time in target timezone today
        target_time_obj = datetime.strptime(target_time_str, "%H:%M").time()
        target_dt = target_tz.localize(datetime.combine(now.date(), target_time_obj))
        
        # Convert to PKT
        pkt_dt = target_dt.astimezone(pkt_tz)
        return pkt_dt.strftime("%H:%M")
    except Exception as e:
        logger.error(f"Error converting time for {target_country}: {e}")
        return target_time_str # Fallback to original time if error


def load_config_from_json(config_path='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise


def get_automation_class(client_config):
    """
    Get the appropriate SalesReportAutomation class based on customized_theme setting.
    
    If customized_theme = 1 AND client exists in theme_config.json: Use customized_automation.py
    Otherwise: Fallback to standard automation.py
    """
    customized_theme = client_config.get('customized_theme', 0)
    client_name = client_config.get('client_name', 'Unknown')
    
    use_customized = False
    if customized_theme == 1:
        # Check if theme exists for this client
        try:
            with open('theme_config.json', 'r') as f:
                theme_config = json.load(f)
            if client_name in theme_config:
                use_customized = True
            else:
                logger.warning(f"Customized theme requested for '{client_name}' but no entry found in theme_config.json. Falling back to STANDARD.")
        except Exception as e:
            logger.error(f"Error checking theme_config.json: {e}. Falling back to STANDARD.")
    
    if use_customized:
        logger.info(f"Using CUSTOMIZED automation for {client_name}")
        from customized_automation import SalesReportAutomation
    else:
        logger.info(f"Using STANDARD automation for {client_name}")
        from automation import SalesReportAutomation
    
    return SalesReportAutomation


def scheduled_job(client_config):
    """Job to run at scheduled time for a specific client"""
    client_name = client_config.get('client_name', 'Unknown')
    try:
        config = load_config_from_json()
        
        # Get appropriate automation class based on customized_theme setting
        SalesReportAutomation = get_automation_class(client_config)
        automation = SalesReportAutomation(config, client_config)
        
        yesterday = datetime.now().strftime('%Y-%m-%d')
        success = automation.run(specific_date=yesterday)
        
        if success:
            logger.info(f"✅ Scheduled sales report for {client_name} generated and sent successfully!")
        else:
            logger.error(f"❌ Scheduled sales report for {client_name} failed")
            
    except Exception as e:
        logger.error(f"Error in scheduled job for {client_name}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


def main():
    """Main entry point for manual execution"""
    try:
        config = load_config_from_json()
        clients = config.get('clients', [])
        
        if not clients:
            print("❌ No clients found in config.json")
            return
            
        yesterday = datetime.now().strftime('%Y-%m-%d')
        
        for client_config in clients:
            client_name = client_config.get('client_name', 'Unknown')
            try:
                # Get appropriate automation class based on customized_theme setting
                SalesReportAutomation = get_automation_class(client_config)
                
                print(f"Executing manual run for {client_name}...")
                automation = SalesReportAutomation(config, client_config)
                
                success = automation.run(specific_date=yesterday)
                
                if success:
                    print(f"✅ Sales report for {client_name} generated and sent successfully!")
                else:
                    print(f"❌ Failed to generate or send sales report for {client_name}")
            except Exception as e:
                print(f"❌ Error processing {client_name}: {str(e)}")
                import traceback
                traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error loading config for manual run: {str(e)}")
        import traceback
        traceback.print_exc()


def start_scheduler():
    """Start the scheduler service to run at configured time daily"""
    try:
        logger.info("Starting scheduler service...")
        config_ = load_config_from_json()
        
        clients = config_.get('clients', [])
        if not clients:
            logger.warning("No clients found in config.json")
            
        for client in clients:
            customized_theme = client.get('customized_theme', 0)
            if customized_theme == 1:
                logger.info(f"📎 Scheduler: {client.get('client_name')} will use CUSTOMIZED automation with dynamic theming")
            else:
                logger.info(f"📎 Scheduler: {client.get('client_name')} will use STANDARD automation")
                
            days_after = client.get('days_after', 1)
            email_time = client.get('email_time', '06:00')
            country = client.get('country', 'PK')
            
            # Calculate PKT time for scheduling
            pkt_trigger_time = get_pkt_time(email_time, country) if country != 'PK' else email_time
            
            schedule.every(days_after).days.at(pkt_trigger_time).do(scheduled_job, client_config=client)
            if country != 'PK':
                logger.info(f"Scheduler configured to run for {client.get('client_name', 'Unknown')} after every {days_after} day at {pkt_trigger_time} PKT (which is {email_time} in {country})")
            else:
                logger.info(f"Scheduler configured to run for {client.get('client_name', 'Unknown')} after every {days_after} day at {email_time}")
            
        logger.info("Scheduler is now active. Press Ctrl+C to stop.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


def load_encrypted_env():
    """Load encrypted environment variables"""
    # Get key from system env (set it manually once)
    key = "sXNET5eRc7oPXUirMSOgd6F78f-z1aacBxmQZYtoIts="
    if not key:
        raise ValueError("Missing ENV_KEY environment variable")

    fernet = Fernet(key.encode())

    with open(".env.enc", "rb") as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)
    load_dotenv(stream=StringIO(decrypted.decode()))


if __name__ == "__main__":
    import sys
    load_encrypted_env()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "schedule":
            start_scheduler()
        elif sys.argv[1] == "manual":
            main()
        else:
            print("Usage:")
            print("  python main.py schedule  - Run as scheduled service")
            print("  python main.py manual    - Run once manually")
    else:
        start_scheduler()

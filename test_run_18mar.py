"""
Test Run Script - Execute Email Service for 18 Mar 2026
This script manually triggers the sales report automation for all clients
for the specific date of March 18, 2026.
"""

import json
import os
import logging
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_encrypted_env():
    """Load encrypted environment variables (Copied from main.py)"""
    key = "sXNET5eRc7oPXUirMSOgd6F78f-z1aacBxmQZYtoIts="
    fernet = Fernet(key.encode())

    try:
        if not os.path.exists(".env.enc"):
            logger.error(".env.enc file not found!")
            return False
            
        with open(".env.enc", "rb") as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted)
        load_dotenv(stream=StringIO(decrypted.decode()))
        logger.info("Encrypted environment variables loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load encrypted env: {e}")
        return False

def load_config_from_json(config_path='config.json'):
    """Load configuration from JSON file (Copied from main.py)"""
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
    Get the appropriate SalesReportAutomation class (Copied from main.py)
    """
    customized_theme = client_config.get('customized_theme', 0)
    client_name = client_config.get('client_name', 'Unknown')
    
    use_customized = False
    if customized_theme == 1:
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

def run_test_for_date(target_date):
    """Main execution for the specific date"""
    print(f"\n{'='*60}")
    print(f"🚀 STARTING TEST RUN FOR DATE: {target_date}")
    print(f"{'='*60}\n")
    
    if not load_encrypted_env():
        print("❌ Error: Could not load environment variables. Aborting.")
        return

    try:
        config = load_config_from_json()
        clients = config.get('clients', [])
        
        if not clients:
            print("❌ No clients found in config.json")
            return
            
        for client_config in clients:
            client_name = client_config.get('client_name', 'Unknown')
            print(f"\n--- Processing Client: {client_name} ---")
            
            try:
                # Get appropriate automation class
                SalesReportAutomation = get_automation_class(client_config)
                
                # Initialize automation
                automation = SalesReportAutomation(config, client_config)
                
                # Run for the specific date
                success = automation.run(specific_date=target_date)
                
                if success:
                    print(f"✅ Sales report for {client_name} generated and sent successfully!")
                else:
                    print(f"❌ Failed to generate or send sales report for {client_name}")
                    
            except Exception as e:
                print(f"❌ Error processing {client_name}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print(f"\n{'='*60}")
        print(f"🏁 TEST RUN COMPLETE")
        print(f"{'='*60}\n")
            
    except Exception as e:
        print(f"❌ Fatal error in test run: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    TEST_DATE = "2026-03-18"
    run_test_for_date(TEST_DATE)

import json
from src.validator import check_distance_accuracy
from src.logger_config import setup_logging

logger = setup_logging()

def run_audit():
    logger.info("Starting Kolkata Map Validation Audit...")
    
    with open('data/landmarks.json', 'r') as f:
        data = json.load(f)
        
    for item in data['landmarks']:
        if 'start' in item:
            real_dist, gap = check_distance_accuracy(item['start'], item['end'], item['app_dist'])
            logger.info(f"Checked: {item['name']} | Real: {real_dist}km | Gap: {gap}km")
            
            if gap > 1.0:
                logger.warning(f"HIGH VARIANCE detected for {item['name']}")

if __name__ == "__main__":
    run_audit()
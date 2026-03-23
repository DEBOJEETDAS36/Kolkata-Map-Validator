# import json
# from src.validator import check_distance_accuracy
# from src.logger_config import setup_logging

# logger = setup_logging()

# def run_audit():
#     logger.info("Starting Kolkata Map Validation Audit...")
    
#     with open('data/landmarks.json', 'r') as f:
#         data = json.load(f)
        
#     for item in data['landmarks']:
#         if 'start' in item:
#             real_dist, gap = check_distance_accuracy(item['start'], item['end'], item['app_dist'])
#             logger.info(f"Checked: {item['name']} | Real: {real_dist}km | Gap: {gap}km")
            
#             if gap > 1.0:
#                 logger.warning(f"HIGH VARIANCE detected for {item['name']}")

# if __name__ == "__main__":
#     run_audit()

from src.engine import GeoAuditEngine
import os

def main():
    # 1. Initialize the Engine with your product parameters
    # A 0.5km threshold makes your product "High Precision"
    engine = GeoAuditEngine(city_name="Kolkata", threshold=0.5)

    # 2. Define your data path
    data_path = os.path.join('data', 'landmarks.json')

    try:
        # 3. Execute the Batch Audit
        # This can now handle 10 or 10,000 landmarks without changing code
        engine.run_batch_audit(data_path)

        # 4. Generate the Market-Ready Report
        # This creates a JSON file in /reports that you can sell to clients
        engine.generate_report()

    except FileNotFoundError:
        engine.logger.error(f"Critical Error: Data file not found at {data_path}")
    except Exception as e:
        engine.logger.error(f"Unexpected System Failure: {str(e)}")

if __name__ == "__main__":
    main()
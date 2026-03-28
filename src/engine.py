import json
import os
from datetime import datetime
from geopy.distance import geodesic
from src.logger_config import setup_logging
from fpdf import FPDF

class GeoAuditEngine:
    def __init__(self, city_name="Kolkata", threshold=1.0):
        """
        Initializes the GeoAudit engine.
        :param city_name: The focus area for the audit.
        :param threshold: The maximum allowed gap (km) before flagging a variance.
        """
        self.city = city_name
        self.threshold = threshold
        self.logger = setup_logging()
        self.audit_results = []

    def calculate_variance(self, start, end, reported_dist):
        """Calculates the gap between ground truth and reported data."""
        # start and end are tuples: (latitude, longitude)
        actual_dist = geodesic(start, end).kilometers
        variance = abs(actual_dist - reported_dist)
        return round(actual_dist, 2), round(variance, 2)

    def run_batch_audit(self, data_file):
        """Processes multiple routes from a JSON database."""
        self.logger.info(f"--- Starting Batch Audit for {self.city} ---")
        
        if not os.path.exists(data_file):
            self.logger.error(f"Data file not found: {data_file}")
            raise FileNotFoundError(f"Missing input: {data_file}")

        with open(data_file, 'r') as f:
            data = json.load(f)

        for item in data['landmarks']:
            try:
                actual, gap = self.calculate_variance(item['start'], item['end'], item['app_dist'])
                status = "PASS" if gap <= self.threshold else "FAIL"
                
                # result = {
                #     "name": item['name'],
                #     "ground_truth_km": actual,
                #     "reported_km": item['app_dist'],
                #     "variance_km": gap,
                #     "status": status,
                #     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # }

                result = {
                    "name": item['name'],
                    "lat": item['end'][0],  # Latitude for the map
                    "lon": item['end'][1],  # Longitude for the map
                    "ground_truth_km": actual,
                    "variance_km": gap,
                    "status": status,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.audit_results.append(result)
                
                log_msg = f"Audited: {item['name']} | Gap: {gap}km | Status: {status}"
                if status == "FAIL":
                    self.logger.warning(log_msg)
                else:
                    self.logger.info(log_msg)
                    
            except KeyError as e:
                self.logger.error(f"Missing data field for {item.get('name', 'Unknown')}: {e}")
            except Exception as e:
                self.logger.error(f"Failed to process {item.get('name', 'Unknown')}: {e}")

    def generate_report(self):
        """Exports the audit results to a JSON report for clients."""
        if not os.path.exists('reports'):
            os.makedirs('reports')
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        report_path = os.path.join('reports', f"audit_report_{timestamp}.json")
        
        with open(report_path, 'w') as f:
            json.dump(self.audit_results, f, indent=4)
        
        self.logger.info(f"Market-ready report generated at: {report_path}")
        print(f"\n✅ Audit Complete. Report saved to {report_path}")


    def export_pdf_report(self):
        """Generates a professional PDF Certificate of the audit."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Header
        pdf.cell(200, 10, txt="GeoAudit Kolkata: Operational Accuracy Report", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(80, 10, "Location Name", 1)
        pdf.cell(40, 10, "Variance (km)", 1)
        pdf.cell(40, 10, "Status", 1)
        pdf.ln()

        # Table Body
        pdf.set_font("Arial", size=10)
        for res in self.audit_results:
            pdf.cell(80, 10, str(res['name']), 1)
            pdf.cell(40, 10, str(res['variance_km']), 1)
            
            # Highlight FAIL in red-like text (optional)
            if res['status'] == "FAIL":
                pdf.set_text_color(255, 0, 0)
            else:
                pdf.set_text_color(0, 0, 0)
                
            pdf.cell(40, 10, str(res['status']), 1)
            pdf.set_text_color(0, 0, 0)
            pdf.ln()

        report_path = f"reports/Certificate_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(report_path)
        return report_path
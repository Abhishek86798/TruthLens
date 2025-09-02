from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def display_report():
    """Display the generated dataset report."""
    report_path = Path("docs/dataset_report.md")
    
    if not report_path.exists():
        logger.error("Report file not found!")
        return False
    
    print("\n=== TruthLens Dataset Report ===\n")
    print(report_path.read_text())
    
    return True

if __name__ == "__main__":
    display_report()

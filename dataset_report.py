import json
import logging
from pathlib import Path
from typing import Dict, List
import statistics
from datetime import datetime
from src.preprocessing import check_data_quality

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ANNOTATION_GUIDELINES = """
# TruthLens Annotation Guidelines

## Label Definitions
- RELIABLE: Claims supported by credible sources, data, or evidence
- UNRELIABLE: Claims lacking support or containing logical fallacies

## Criteria
1. Source Credibility
2. Evidence Quality
3. Logical Consistency
"""

def load_dataset(path: str) -> List[Dict]:
    """Load dataset from JSONL file."""
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def generate_stats(dataset: List[Dict]) -> Dict:
    """Generate dataset statistics."""
    text_lengths = [len(item['text'].split()) for item in dataset]
    label_counts = {}
    
    for item in dataset:
        label = item['label']
        label_counts[label] = label_counts.get(label, 0) + 1
    
    return {
        "total_examples": len(dataset),
        "avg_length": statistics.mean(text_lengths),
        "median_length": statistics.median(text_lengths),
        "label_distribution": label_counts,
        "quality_metrics": check_data_quality(dataset)
    }

def generate_report(dataset_path: str, output_path: str) -> bool:
    """Generate markdown report for dataset."""
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        dataset = load_dataset(dataset_path)
        stats = generate_stats(dataset)
        
        report = f"""# TruthLens Dataset Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview
- Total Examples: {stats['total_examples']}
- Average Text Length: {stats['avg_length']:.1f} words
- Median Text Length: {stats['median_length']:.1f} words

## Label Distribution
{'-' * 40}
"""
        for label, count in stats['label_distribution'].items():
            percentage = (count / stats['total_examples']) * 100
            report += f"- {label}: {count} ({percentage:.1f}%)\n"
        
        report += f"\n## Quality Metrics\n{'-' * 40}\n"
        for key, value in stats['quality_metrics'].items():
            if key != 'issues':
                report += f"- {key}: {value}\n"
        
        report += f"\n## Annotation Guidelines\n{ANNOTATION_GUIDELINES}"
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        logger.info(f"Report generated: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        return False

def test_report_generation():
    """Test report generation with sample data."""
    # Create test data
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    test_dataset = [
        {
            "id": "1",
            "text": "This is a reliable test entry with sufficient content for testing. " * 3,
            "label": "RELIABLE"
        },
        {
            "id": "2",
            "text": "This is an unreliable test entry that should be counted. " * 2,
            "label": "UNRELIABLE"
        }
    ]
    
    # Save test dataset
    dataset_path = test_dir / "test_dataset.jsonl"
    with open(dataset_path, 'w', encoding='utf-8') as f:
        for item in test_dataset:
            f.write(json.dumps(item) + '\n')
    
    # Generate report
    report_path = test_dir / "test_report.md"
    success = generate_report(str(dataset_path), str(report_path))
    
    # Verify report exists and contains required sections
    if success and report_path.exists():
        content = report_path.read_text()
        assert "Dataset Overview" in content
        assert "Label Distribution" in content
        assert "Quality Metrics" in content
        logger.info("✓ Report generation test passed")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    return success

if __name__ == "__main__":
    test_report_generation()

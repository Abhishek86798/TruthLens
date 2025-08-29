import arxiv
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class SourceType(Enum):
    SCIENTIFIC = "scientific"
    GOVERNMENT = "government"
    NEWS = "news"
    SOCIAL_MEDIA = "social_media"
    BLOG = "blog"

@dataclass
class DataSource:
    text: str
    url: str
    source_type: SourceType
    credibility_score: float
    is_factual: bool

class DatasetBuilder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sources: Dict[SourceType, List[DataSource]] = {st: [] for st in SourceType}
    
    def collect_arxiv_papers(self, query: str, max_results: int = 100) -> List[DataSource]:
        """Collect papers from arxiv.org"""
        self.logger.info(f"Collecting arxiv papers for query: {query}")
        
        papers = []
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for paper in arxiv.Client().results(search):
                papers.append(DataSource(
                    text=f"Title: {paper.title}\nAbstract: {paper.summary}",
                    url=paper.entry_id,
                    source_type=SourceType.SCIENTIFIC,
                    credibility_score=0.9,
                    is_factual=True
                ))
                
            self.logger.info(f"Collected {len(papers)} papers")
            
        except Exception as e:
            self.logger.error(f"Error collecting papers: {e}")
            
        return papers

    async def collect_government_reports(self, domains: List[str]) -> List[DataSource]:
        """Collect reports from .gov domains"""
        # Implementation for government sources
        pass

    async def collect_news_articles(self, domains: List[str]) -> List[DataSource]:
        """Collect articles from reputable news sources"""
        # Implementation for news sources
        pass

    def balance_dataset(self, target_size: int = 1000) -> List[DataSource]:
        """Create balanced dataset with equal distribution"""
        balanced_data = []
        per_category = target_size // len(SourceType)
        
        for source_type in SourceType:
            available = self.sources[source_type]
            if len(available) > per_category:
                balanced_data.extend(available[:per_category])
            else:
                # Need to implement data augmentation here
                balanced_data.extend(available)
        
        return balanced_data

    def save_dataset(self, output_file: str):
        """Save balanced dataset to file"""
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_samples': len(self.sources),
                    'distribution': {st.value: len(self.sources[st]) 
                                  for st in SourceType}
                },
                'data': [{'text': s.text, 'source_type': s.source_type.value,
                         'credibility': s.credibility_score, 
                         'is_factual': s.is_factual}
                        for sources in self.sources.values()
                        for s in sources]
            }, f, indent=2, ensure_ascii=False)

def main():
    try:
        # Initialize builder
        builder = DatasetBuilder()
        
        # Collect papers
        scientific_papers = builder.collect_arxiv_papers(
            "climate change OR machine learning"
        )
        builder.sources[SourceType.SCIENTIFIC].extend(scientific_papers)
        
        # Balance and save dataset
        balanced_data = builder.balance_dataset()
        builder.save_dataset('training_data.json')
        
        print(f"Generated balanced dataset with {len(balanced_data)} samples")
        return balanced_data
        
    except Exception as e:
        logger.error(f"Dataset generation failed: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    result = main()
    if result is not None:
        print("✅ Dataset generation completed successfully")
    else:
        print("❌ Dataset generation failed")

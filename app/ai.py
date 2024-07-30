from transformers import pipeline
from schemas.sentiment_schemas import SentimentScore, SentimentRequest, SentimentResponse
from loguru import logger

class SentimentAnalyzer:
    def __init__(self):
        # Load the sentiment analysis pipeline with the specified model
        self.sentiment_analyzer = pipeline("text-classification", model="avichr/heBERT_sentiment_analysis", top_k=None)

    def analyze_sentiment(self, sentiment: SentimentRequest) -> SentimentResponse:
        logger.info(f"Analyzing sentiment for: {sentiment.text}")
        analysis = self.sentiment_analyzer(sentiment.text)

        # Convert the analysis results to a list of SentimentScore objects
        results = [SentimentScore(label=item['label'], score=item['score']) for item in analysis[0]]
        top_result = max(results, key=lambda x: x.score)

        logger.info(f"Analysis results: {results}")
        logger.info(f"Top result: {top_result}")

        return SentimentResponse(text=sentiment.text, results=results, top_result=top_result)
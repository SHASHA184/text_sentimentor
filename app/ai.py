from transformers import pipeline
from schemas import SentimentScore, SentimentRequest, SentimentResponse

class SentimentAnalyzer:
    def __init__(self):
        # Load the sentiment analysis pipeline with the specified model
        self.sentiment_analyzer = pipeline("text-classification", model="avichr/heBERT_sentiment_analysis", top_k=None)

    def analyze_sentiment(self, sentiment: SentimentRequest) -> SentimentResponse:
        analysis = self.sentiment_analyzer(sentiment.text)

        # Convert the analysis results to a list of SentimentScore objects
        results = [SentimentScore(label=item['label'], score=item['score']) for item in analysis[0]]
        top_result = max(results, key=lambda x: x.score)

        return SentimentResponse(text=sentiment.text, results=results, top_result=top_result)
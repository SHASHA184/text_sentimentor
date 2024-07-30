from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Sentiment
from schemas.sentiment_schemas import SentimentResponse
from database import get_db
from loguru import logger


app = FastAPI()

@app.post("/sentiments/", response_model=SentimentResponse)
async def create_sentiment(sentiment: SentimentResponse, db: Session = Depends(get_db)):
    try:
        analysis = await Sentiment.create(db, sentiment)
        return analysis
    except Exception as e:
        return {"error": str(e)}
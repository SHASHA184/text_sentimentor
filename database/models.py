from sqlalchemy import Column, Integer, String, Float
from database import Base
from schemas.sentiment_schemas import SentimentResponse
from loguru import logger

class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    neutral = Column(Float)
    positive = Column(Float)
    negative = Column(Float)

    @classmethod
    async def create(cls, db_session, sentiment: SentimentResponse) -> SentimentResponse:
        new_sentiment = cls(
            text=sentiment.text,
            neutral=sentiment.results[0].score,
            positive=sentiment.results[1].score,
            negative=sentiment.results[2].score
        )
        db_session.add(new_sentiment)
        await db_session.commit()
        await db_session.refresh(new_sentiment)

        return SentimentResponse.from_db(
            id=new_sentiment.id,
            text=new_sentiment.text,
            neutral=new_sentiment.neutral,
            positive=new_sentiment.positive,
            negative=new_sentiment.negative
        )
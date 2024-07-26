from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from app.ai import SentimentAnalyzer
from app.schemas import SentimentRequest, SentimentResponse, SentimentScore
from app.database import get_db
from app.models import Sentiment
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_model=SentimentResponse)
async def analyze_sentiment_view(sentiment: SentimentRequest = Depends(SentimentRequest.as_form), db: Session = Depends(get_db)):
    analysis = SentimentAnalyzer().analyze_sentiment(sentiment)
    await Sentiment.create(db, analysis)
    return analysis

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

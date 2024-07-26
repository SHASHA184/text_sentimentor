from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from ai import SentimentAnalyzer
from schemas import SentimentRequest, SentimentResponse, SentimentScore
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_model=SentimentResponse)
async def analyze_sentiment_view(sentiment: SentimentRequest = Depends(SentimentRequest.as_form)):
    analysis = SentimentAnalyzer().analyze_sentiment(sentiment)
    return analysis

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

from fastapi import FastAPI, Request, Depends,  HTTPException
from fastapi.templating import Jinja2Templates
from ai import SentimentAnalyzer
from schemas.sentiment_schemas import SentimentRequest, SentimentResponse, SentimentScore
import uvicorn
import aiohttp
from loguru import logger
from pydantic import ValidationError

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DATABASE_API_URL = "http://database:8081"

@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_model=SentimentResponse)
async def analyze_sentiment_view(sentiment: SentimentRequest = Depends(SentimentRequest.as_form)):
    analysis = SentimentAnalyzer().analyze_sentiment(sentiment)

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{DATABASE_API_URL}/sentiments/", json=analysis.model_dump()) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to save sentiment")
            response_data = await response.json()
            try:
                return SentimentResponse(**response_data)
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                raise HTTPException(status_code=500, detail="Invalid response format")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

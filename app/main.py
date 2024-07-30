from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from ai import SentimentAnalyzer
from schemas.sentiment_schemas import (
    SentimentRequest,
    SentimentResponse,
    SentimentScore,
)
import uvicorn
import aiohttp
from loguru import logger
from pydantic import ValidationError
from config import DATABASE_API_URL
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError, StarletteHTTPException

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # Extract the first error message
    error_message = exc.errors()[0].get('msg', 'Invalid input')
    return templates.TemplateResponse("error.html", {"request": request, "message": error_message}, status_code=422)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "message": exc.detail},
        status_code=exc.status_code
    )

@app.get("/")
async def read_form(request: Request):
    # Render the form HTML template
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/", response_model=SentimentResponse, response_class=HTMLResponse)
async def analyze_sentiment_view(
    request: Request,
    sentiment: SentimentRequest = Depends(SentimentRequest.as_form),
):
    # Analyze sentiment
    analysis = SentimentAnalyzer().analyze_sentiment(sentiment)

    # Save the result to the database API
    async with aiohttp.ClientSession() as session:
        # Send a POST request to the database API to save the sentiment
        async with session.post(
            f"{DATABASE_API_URL}/sentiments/", json=analysis.model_dump()
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status, detail="Failed to save sentiment"
                )
            response_data = await response.json()
            try:
                # Create a SentimentResponse object from the response data
                sentiment_response = SentimentResponse(**response_data)
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                raise HTTPException(status_code=500, detail="Invalid response format")

    # Render the HTML response with the results
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "text": sentiment_response.text,
            "results": sentiment_response.results,
            "top_result": sentiment_response.top_result,
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

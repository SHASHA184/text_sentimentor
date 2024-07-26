from pydantic import BaseModel, Field, field_validator
from typing import List
from fastapi import Form
from enum import Enum

class SentimentLabel(str, Enum):
    NEUTRAL = 'neutral'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'

class SentimentScore(BaseModel):
    label: SentimentLabel
    score: float

class SentimentRequest(BaseModel):
    text: str

    @classmethod
    def as_form(cls, text: str = Form(...)):
        return cls(text=text)

class SentimentResponse(BaseModel):
    text: str
    results: List[SentimentScore]
    top_result: SentimentScore

from pydantic import BaseModel, Field, field_validator
from typing import List
from fastapi import Form
from enum import Enum
from typing import Optional

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

    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text must not be empty')
        return v
    
    @field_validator('text')
    def text_must_be_shorter_than_1000_characters(cls, v):
        if len(v) > 1000:
            raise ValueError('Text must be shorter than 1000 characters')
        return v

class SentimentResponse(BaseModel):
    id: Optional[int] = None
    text: str
    results: List[SentimentScore]
    top_result: SentimentScore

    @classmethod
    def from_db(cls, id: int, text: str, neutral: float, positive: float, negative: float):
        scores = [
            SentimentScore(label="neutral", score=neutral),
            SentimentScore(label="positive", score=positive),
            SentimentScore(label="negative", score=negative),
        ]
        top_result = max(scores, key=lambda x: x.score)
        return cls(id=id, text=text, results=scores, top_result=top_result)
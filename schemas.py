from typing import List

from pydantic import BaseModel, Field


class ExtractedAnswer(BaseModel):
    """Answer the question."""

    question: str = Field(description="The question to be changed")
    answer: str = Field(description="The extracted answer for the question")

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}"


class OutputAnswer(BaseModel):
    """Answer the question."""

    message: str = Field(description="Message to the user")

    def __str__(self):
        return f"Message: {self.message}"

from typing import List, Dict, Any, Optional
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class SurveyResponse(BaseModel):
    """Model for survey question responses"""
    finished: bool = Field(
        description="Whether the value is saved to database")
    message: str = Field(
        description="Message to user")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finished": self.finished,
            "message": self.message
        }


class SurveyChange(BaseModel):
    """Model for survey changes requested by user"""
    question: str = Field(description="The question to be changed")
    answer: str = Field(description="The new answer for the question")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "answer": self.answer
        }


class SurveySummary(BaseModel):
    """Model for survey summary response"""
    status: str = Field(
        description="'OK' if everything is correct, 'CHANGES' if changes requested")
    changes: Optional[List[SurveyChange]] = Field(
        default=None,
        description="List of changes requested by user, only if status is 'CHANGES'"
    )

    def to_dict(self) -> Dict[str, Any]:
        result = {"status": self.status}
        if self.changes:
            result["changes"] = [change.to_dict() for change in self.changes]
        return result


# Create parsers
survey_response_parser = PydanticOutputParser(pydantic_object=SurveyResponse)
survey_summary_parser = PydanticOutputParser(pydantic_object=SurveySummary)

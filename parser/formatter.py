from questions.questions import Questions
from parser.output_parsers import survey_summary_parser
import os

SHOW_LOGS = os.getenv("SHOW_ALL_LOGS", False)


def parse_summary_changes(result: str):
    """Programowo odczytuje zmiany z odpowiedzi agenta."""
    try:
        # Próbujemy sparsować odpowiedź jako SurveySummary
        parsed_result = survey_summary_parser.parse(result)
        if SHOW_LOGS:
            print(f"Parsed result: {parsed_result}")
        if parsed_result.status == "OK":
            return []
        elif parsed_result.status == "CHANGES" and parsed_result.changes:
            return [change.to_dict() for change in parsed_result.changes]
        else:
            return []
    except Exception as e:
        print(f"Error parsing summary: {e}")
        return []


def format_summary(db):
    mapping = {v["db_key"]: q for q, v in Questions.QUESTIONS.items()}
    return "\n".join(
        f"{mapping[k]}: {v}" for k, v in db.items() if v is not None
    )

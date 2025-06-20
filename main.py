from Config import Config
from parser.formatter import parse_summary_changes
from parser.output_parsers import survey_response_parser
from agents.summary_agent import create_survey_summary_agent, process_survey_summary
from agents.question_agent import create_survey_agent, process_survey_question
from questions.questions import Questions
from dotenv import load_dotenv

load_dotenv()

config = Config()


def user_survey(agent, questions: list[str], user_input: str = None):
    get_input = user_input is None
    for question in questions:
        # ASK USER
        if get_input:
            print(f"\n{question}\n")
        while True:
            if get_input:
                # GET USER INPUT
                user_input = input()
            result = process_survey_question(agent, question, user_input)
            if config.show_logs:
                print(f"Result: {result}")

            try:
                parsed_result = survey_response_parser.parse(result)
                message = parsed_result.message
                print(message)
                get_input = True
                if parsed_result.finished:
                    break
            except Exception as e:
                print(f"Błąd parsowania odpowiedzi: {e}")


def user_summary(question_agent, summary_agent):
    while True:
        print(f"\nTwoje dane: {Questions.MOCK_DB}")

        print("\nCzy wszystko się zgadza? Jeśli nie, napisz co chcesz zmienić:")

        user_input = input()
        result = process_survey_summary(
            summary_agent, Questions.MOCK_DB, user_input)
        if config.show_logs:
            print(f"Wynik podsumowania: {result}")
        try:
            changes = parse_summary_changes(result)
            if config.show_logs:
                print(f"Zmiany: {changes}")
            if not changes:
                if config.show_logs:
                    print("Summary agent zakończył ankietę!")
                return

            if config.show_logs:
                print("\nWykryte zmiany:")
            for change in changes:
                user_survey(question_agent, [
                            change["question"]], change["answer"])

        except Exception:
            print("Brak zmian lub odpowiedź OK.")


if __name__ == "__main__":
    print(
        f"Czesc! Oto pytania, ktore musisz odpowiedziec:\n{Questions.get_all_questions()}\n Zaczynajmy!")

    question_agent = create_survey_agent()
    summary_agent = create_survey_summary_agent()

    user_survey(question_agent, Questions.QUESTIONS.keys())

    user_summary(question_agent, summary_agent)

    print(f"\nCo zapisano w bazie danych: {Questions.MOCK_DB}")

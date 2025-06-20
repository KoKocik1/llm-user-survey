# 🤖 llm-user-survey

A conversational user survey system powered by a Large Language Model (LLM). This tool guides the user through answering personal questions in natural language, validates the responses, and generates a summary with an option to make corrections. Built with LangChain and OpenAI.

---

## 🧠 How it works

1. The user answers questions in natural language.
2. The system validates and processes answers using an LLM agent.
3. After summarizing the data, the user can say: "that's wrong, I'm a woman and I weigh 42 kg" – and the agent will update the respective fields.
4. Final structured data is printed or stored.

---

## ✅ Requirements

- Python 3.9+
- OpenAI API key
- (Optional) `.env` file for configuration

---

## ⚙️ Installation

```bash
git clone https://github.com/KoKocik1/llm-user-survey.git
cd llm-user-survey
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🔐 Configuration

Create a `.env` file (or export variables), e.g.: `.env.egample`

> 💡 Only `OPENAI_API_KEY` is required. The rest is optional.

To enable agent logs:

```env
SHOW_LANGCHAIN_LOGS=True
```

---

## 🚀 Run

```bash
python main.py
```

---

## 🧪 Sample Questions

```text
What is your weight in kg?
What is your year of birth?
What is your gender?
Do you have allergies? If so, list them.
```

---

## 🧭 Demo

### Sample run:

```
What is your weight in kg?
> I weigh 41
Saved 41 to database.

What is your year of birth?
> I was born in 1300
Validation failed. Please enter a year between 1925 and 2025.
> 1999
Saved 1999 as your birth year.

...

Is everything correct? If not, say what you'd like to change:
> I weigh 411 kg, I was born 2000
Validation failed. Please enter a year between 1925 and 2025.
> 42
Saved 42 kg to the database.
Saved 2000 as your birth year.
```

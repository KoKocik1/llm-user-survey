# LLM User Survey Agent

A LangChain-based agent that processes user responses to survey questions with intelligent validation and database storage.

## Features

- **Intelligent Response Processing**: Uses LangChain agents to extract and validate user responses
- **Range Validation**: Validates numeric responses against specified ranges
- **Database Integration**: Automatically saves processed responses to a mock database
- **Error Handling**: Provides clear feedback for invalid or unclear responses
- **Multi-language Support**: Handles Polish responses for various question types

## Question Types Supported

1. **Weight Questions**: Extracts weight in kg (range: 10-200 kg)
2. **Year Questions**: Extracts birth year (range: current_year-100 to current_year)
3. **Gender Questions**: Normalizes to M (male) or K (female)
4. **Allergy Questions**: Extracts allergies or returns 'nie' if none

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

Run the survey:

```bash
python main.py
```

The agent will:

1. Ask each question in sequence
2. Process your response using appropriate tools
3. Validate ranges where applicable
4. Save results to the database
5. Provide feedback on the processing result

## Response Processing

- **OK**: Response successfully processed and saved
- **nie rozumiem**: Agent couldn't understand the response
- **out of range**: Value is outside the acceptable range
- **Error**: Technical error occurred during processing

## Database Structure

The mock database stores responses in the following format:

```python
MOCK_DB = {
    "waga": None,        # Weight in kg
    "rok_urodzenia": None, # Birth year
    "plec": None,        # Gender (M/K)
    "alergie": None      # Allergies or 'nie'
}
```

## Tools Available

- `validate_range`: Validates numeric values against ranges
- `save_to_database`: Saves processed answers to the database
- `get_question_instruction`: Retrieves specific processing instructions
- `extract_number_from_text`: Extracts numbers from text
- `extract_year_from_text`: Extracts 4-digit years
- `normalize_gender`: Normalizes gender responses
- `extract_allergies`: Extracts allergy information

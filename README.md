## Buddhist Scripture Explanation API
This is a Flask-based API that leverages OpenAI's GPT-4 to provide explanations for passages from various Buddhist scriptures. The API supports both Chinese and English languages.

## Features
- Multi-language Support: Explain scriptures in either Chinese or English.
- Multiple Scriptures: Supports popular Buddhist scriptures like the Heart Sutra, Diamond Sutra, Śūraṅgama Sūtra, and more.
- Customizable Responses: The model can be fine-tuned with different temperatures to adjust the creativity of the responses.

## Setup
Prerequisites
Python 3.11
An OpenAI API key

Create .env file in repo and put your openai key as below:
OPENAI_API_KEY=<your-openai-api-key>

## virtual environment
``` bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## run app
run.sh
```

## Request Body
``` json
{
  "scripture": "Heart Sutra",
  "text": "Here is the passage you want to explain.",
  "language": "zh"  # or "en" for English
}
```

## local test

curl -X POST http://127.0.0.1:5000/explain -H "Content-Type: application/json" -d '{
  "scripture": "心经",
  "text": "色不异空，空不异色；色即是空，空即是色。",
  "language": "zh"
}'


## Contributing
If you have any ideas or suggestions to improve this API, feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.


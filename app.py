from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()
if not openai.api_key:
    raise ValueError("OpenAI API key not set. Please ensure it is in the .env file.")   

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# 中英文经文对照表
scriptures = {
    "zh": {
        "Heart Sutra": "心经",
        "Diamond Sutra": "金刚经",
        "Śūraṅgama Sūtra": "楞严经",
        "Vimalakīrti Sūtra": "维摩诘经",
        "Lankavatara Sutra": "楞伽经",
        "Platform Sutra": "六祖坛经",
        "Perfect Enlightenment Sutra": "圆觉经"
    },
    "en": {
        "Heart Sutra": "Heart Sutra",
        "Diamond Sutra": "Diamond Sutra",
        "Śūraṅgama Sūtra": "Śūraṅgama Sūtra",
        "Vimalakīrti Sūtra": "Vimalakīrti Sūtra",
        "Lankavatara Sutra": "Lankavatara Sutra",
        "Platform Sutra": "Platform Sutra",
        "Perfect Enlightenment Sutra": "Perfect Enlightenment Sutra"
    }
}

@app.route('/explain', methods=['POST'])
def explain_scripture():
    try:
        data = request.json
        scripture_key = data.get("scripture")
        passage = data.get("text")
        language = data.get("language", "zh")  # 默认语言为中文

        # 根据语言选择经文名称
        scripture_name = scripture_key
        if language == "zh":
            scripture_name = {v: k for k, v in scriptures['zh'].items()}.get(scripture_key)
        else:
            scripture_name = scripture_key

        if not scripture_name:
            return jsonify({"error": "Invalid scripture or language"}), 400

        # 根据选择的语言构造消息
        if language == "zh":
            messages = [
                {"role": "system", "content": "你是一个专业的佛学解释者，擅长解释佛经。"},
                {"role": "user", "content": f"请解释以下《{scripture_name}》中的段落:\n\n{passage}"}
            ]
        else:
            messages = [
                {"role": "system", "content": "You are a knowledgeable expert in explaining Buddhist scriptures."},
                {"role": "user", "content": f"Please explain the following passage from the {scripture_name}:\n\n{passage}"}
            ]

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.7  # 温度值越高，生成的内容越具创造性
        )

        explanation = response['choices'][0]['message']['content'].strip()
        return jsonify({"explanation": explanation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
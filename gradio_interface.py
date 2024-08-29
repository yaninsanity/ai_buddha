import gradio as gr
import requests

# Flask 后端服务器 URL
backend_url = "http://127.0.0.1:5000/explain"

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

def get_scripture_options(language):
    return list(scriptures[language].values())

def get_explanation(scripture, passage, language):
    data = {
        "scripture": scripture,
        "text": passage,
        "language": language
    }
    response = requests.post(backend_url, json=data)
    if response.status_code == 200:
        return response.json().get("explanation")
    else:
        return response.json().get("error", "Error: Unable to generate explanation.")

def update_scripture_options(language):
    return gr.Dropdown.update(choices=get_scripture_options(language))

# 定义 Gradio 界面
with gr.Blocks() as iface:
    language = gr.Dropdown(choices=["zh", "en"], label="Language (语言)", value="zh")
    scripture = gr.Dropdown(choices=get_scripture_options("zh"), label="Select Scripture (选择经文)")
    passage = gr.Textbox(lines=5, label="Input Passage (输入段落)")
    explanation = gr.Textbox(label="Explanation (解释)")

    language.change(fn=update_scripture_options, inputs=language, outputs=scripture)
    generate_button = gr.Button("Generate Explanation (生成解释)")

    generate_button.click(
        fn=get_explanation, 
        inputs=[scripture, passage, language], 
        outputs=explanation
    )

iface.launch()

from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

def is_complaint(question):
    # 푸념 여부를 판단하기 위한 프롬프트 설정
    messages = [
        {"role": "system", "content": "Determine if the following statement is a complaint or venting without a clear purpose:"},
        {"role": "user", "content": f"Statement: \"{question}\"\nIs this statement a complaint or venting? Answer \"yes\" or \"no\"."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        max_tokens=10,
        temperature=0.5,
    )
    
    return "yes" in response.choices[0].message['content'].strip().lower()

def is_flirting_with_min_yong(question):
    # 플러팅 여부를 판단하기 위한 프롬프트 설정
    messages = [
        {"role": "system", "content": "Determine if the following statement is flirtatious towards a person named Min Yong."},
        {"role": "user", "content": f"Statement: \"{question}\"\nIs this statement flirtatious towards Min Yong? Answer \"yes\" or \"no\"."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        max_tokens=10,
        temperature=0.5,
    )
    
    return "yes" in response.choices[0].message['content'].strip().lower()

def generate_min_yong_response(question):
    # 민용적 사고 스타일의 답변을 생성하는 프롬프트 설정
    messages = [
        {"role": "system", "content": "당신은 민용입니다. 냉소적이고 직설적인 답변으로 유명한 사람입니다."},
        {"role": "user", "content": f"Question: {question}\nResponse:"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        max_tokens=60,
        temperature=0.7,
    )
    
    answer = response.choices[0].message['content'].strip()

    if is_flirting_with_min_yong(question):
        answer += " 개수작 부리지 마."
    
    return answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        data = request.get_json()
        question = data['question']
        response = generate_min_yong_response(question)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
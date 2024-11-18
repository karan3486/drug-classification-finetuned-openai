from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
client = OpenAI()
# Configure your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to get the response from the model
def get_answer(question):
  response=client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::AUoSlJWs",
    messages=[{"role": "system", "content": "You are a medical assistant specializing in drug and malady classification. You help classify drugs and match them with possible ailments."}, 
              {"role": "user", "content": question}]
  )
  return response.choices[0].message.content
mapping_value = {'Acne': '0',
 'Adhd': '1',
 'Allergies': '2',
 'Alzheimer': '3',
 'Amoebiasis': '4',
 'Anaemia': '5',
 'Angina': '6'}
drug_class = {value: key for key, value in mapping_value.items()}
# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to handle chatbot messages
@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    answer = get_answer(question)
    val = drug_class.get(answer.strip())
    final_answer = str(answer + ': ' + val)
    return jsonify({'answer': final_answer})

if __name__ == '__main__':
    app.run(debug=True)

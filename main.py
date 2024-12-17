from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

def save_to_json(data):
    try:
        with open('responses.json', 'r', encoding='utf-8') as f:
            responses = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        responses = []
    
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    responses.append(data)
    
    with open('responses.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        form_data = {
            'grade': request.form.get('grade'),
            'frequency': request.form.get('frequency'),
            'usage': request.form.getlist('usage'),
            'accuracy': request.form.get('accuracy'),
            'without_ai': request.form.get('without_ai'),
            'pros_cons': request.form.get('pros_cons', '').strip()
        }
        
        try:
            save_to_json(form_data)
            return jsonify({'success': True, 'message': 'კითხვარი წარმატებით გაიგზავნა!'})
        except Exception as e:
            print(f"Error saving form data: {e}")
            return jsonify({'success': False, 'message': 'დაფიქსირდა შეცდომა, სცადეთ თავიდან'}), 500
    
    return jsonify({'success': False, 'message': 'არასწორი მოთხოვნა'}), 400

if __name__ == '__main__':
    app.run(debug=True)
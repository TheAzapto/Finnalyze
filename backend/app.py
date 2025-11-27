from flask import Flask, jsonify, request
import json
from FinLlama_Middleware import Summarize, Evaluate

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def get_impact_score():
    try:
        article = request.json.get('article')
        if not article:
            return jsonify({'error': 'Article is required'}), 400
    
        print('Generating Summary')
        summary = Summarize(article)
        print('Generating Impact Scores')
        impact_scores = json.loads(Evaluate(summary))

        return impact_scores, 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

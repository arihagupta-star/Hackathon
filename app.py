from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    # Simulate a chatbot response
    response = {'response': f'You said: {user_message}'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
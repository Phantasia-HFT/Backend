from flask import Flask, render_template, request, jsonify
from agents import get_content

app = Flask(__name__)

@app.route('/getscript', methods=['POST'])
def get_script():
    if request.method == 'POST':
        # Assuming the incoming data is JSON
        data = request.get_json()  # This will parse the JSON body
        
        # Example of extracting user input (make sure it's passed as a key in the JSON body)
        user_input = data.get('user_input')
        
        if user_input:
            script = get_content(user_input)  # Assuming your get_content function handles the input
            return jsonify({"script": script}), 200  # Return the generated script as a JSON response
        else:
            return jsonify({"error": "No user_input provided"}), 400

if __name__ == '__main__':
    app.run()

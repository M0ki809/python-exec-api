from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Python Exec API is running!"

@app.route('/execute', methods=['POST', 'GET'])  # Добавили GET
def execute():
    if request.method == 'GET':
        return jsonify({"status": "GET allowed for test"})
    try:
        data = request.get_json()
        code = data.get("code", "")
        local_vars = {}
        exec(code, {}, local_vars)
        result = local_vars.get("result", "No result variable")
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)})

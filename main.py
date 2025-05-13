from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    data = request.get_json()
    code = data.get("code", "")

    local_vars = {}

    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", None)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return "Python Exec API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

import os
import io
import traceback
from flask import Flask, request, jsonify
import contextlib

app = Flask(__name__)

@app.route('/')
def home():
    return "Python Exec API is running!"

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'GET':
        return jsonify({"status": "GET allowed for test"})
    
    try:
        data = request.get_json()
        code = data.get("code", "")
        local_vars = {}

        # буфер для перехвата stdout (print)
        output_buffer = io.StringIO()
        
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {}, local_vars)
        
        printed_output = output_buffer.getvalue().strip()
        result = local_vars.get("result", None)

        response = {}
        if result is not None:
            response["result"] = result
        if printed_output:
            response["print"] = printed_output
        if not response:
            response["info"] = "Код выполнен, но ничего не выведено и переменная result не задана."

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

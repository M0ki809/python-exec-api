import os
import io
import sys
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Python Base64 Exec API is running!"

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        code_b64 = data.get("code", "")
        code = base64.b64decode(code_b64).decode("utf-8")

        # Подготовка stdout к перехвату вывода print()
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        local_vars = {}

        try:
            compiled = compile(code, "<string>", "exec")
            exec(compiled, {}, local_vars)
        except Exception as e:
            sys.stdout = old_stdout
            return jsonify({"error": f"Execution error: {str(e)}"})

        # Сохраняем вывод print'ов
        printed_output = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout

        result = local_vars.get("result")
        last_expr_result = None
        try:
            last_line = code.strip().splitlines()[-1]
            last_expr_result = eval(last_line, {}, local_vars)
        except:
            pass

        response = {}
        if printed_output:
            response["print"] = printed_output
        if result is not None:
            response["result"] = result
        if last_expr_result is not None and result != last_expr_result:
            response["expression_result"] = last_expr_result

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"General error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

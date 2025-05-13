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

        # Перехват stdout для print()
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        local_vars = {}

        try:
            compiled = compile(code, "<string>", "exec")
            exec(compiled, {}, local_vars)
        except Exception as e:
            sys.stdout = old_stdout
            return jsonify({"result": f"Execution error: {str(e)}"})

        # Сохраняем вывод print
        printed_output = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout

        result = local_vars.get("result")
        last_expr_result = None
        try:
            last_line = code.strip().splitlines()[-1]
            last_expr_result = eval(last_line, {}, local_vars)
        except:
            pass

        # Формируем итоговый ответ
        if result is not None:
            final_result = result
        elif last_expr_result is not None:
            final_result = last_expr_result
        elif printed_output:
            final_result = printed_output
        else:
            final_result = "No result returned"

        return jsonify({"result": final_result})

    except Exception as e:
        return jsonify({"result": f"General error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

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
        code = data.get("code", "").strip()
        local_vars = {}

        output_buffer = io.StringIO()
        last_expr_result = None

        with contextlib.redirect_stdout(output_buffer):
            # Попробуем отдельно вычислить последнюю строку как выражение
            lines = code.split('\n')
            *body_lines, last_line = lines

            body_code = '\n'.join(body_lines).strip()
            if body_code:
                exec(body_code, {}, local_vars)

            # Попробуем вычислить последнюю строку
            try:
                last_expr_result = eval(last_line, {}, local_vars)
            except:
                # Если не выражение — выполнить как код
                exec(last_line, {}, local_vars)

        printed_output = output_buffer.getvalue().strip()
        result = local_vars.get("result", None)

        response = {}
        if result is not None:
            response["result"] = result
        if last_expr_result is not None:
            response["expression_result"] = last_expr_result
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

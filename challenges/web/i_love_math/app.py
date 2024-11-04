from flask import Flask, request, render_template_string
import subprocess
import html

app = Flask(__name__)

PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Calculator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 600px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .calculator-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .span-2 {
            grid-column: span 2;
        }
        button {
            padding: 10px;
            font-size: 1.1rem;
            border: none;
            background: #3498db;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #2980b9;
        }
        .display {
            grid-column: 1 / -1;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: right;
            font-size: 1.5rem;
            margin-bottom: 10px;
            border: 1px solid #dee2e6;
        }
        .history {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .history h3 {
            margin-top: 0;
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .result-item {
            padding: 8px;
            border-bottom: 1px solid #dee2e6;
        }
        .result-item:last-child {
            border-bottom: none;
        }
        .advanced-options {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .advanced-options input {
            width: calc(50% - 10px);
            padding: 8px;
            margin: 5px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
        }
        .advanced-options button {
            width: 100%;
            margin-top: 10px;
            background: #2ecc71;
        }
        .advanced-options button:hover {
            background: #27ae60;
        }
        .input-group {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .input-group label {
            margin-right: 10px;
            min-width: 120px;
        }
        .input-group input {
            flex: 1;
            padding: 8px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculator</h1>
        <div class="calculator-grid">
            <div class="display" id="display">0</div>
            <button onclick="clearDisplay()">C</button>
            <button onclick="appendToDisplay('(')">(</button>
            <button onclick="appendToDisplay(')')">)</button>
            <button onclick="appendToDisplay('/')">/</button>
            <button onclick="appendToDisplay('7')">7</button>
            <button onclick="appendToDisplay('8')">8</button>
            <button onclick="appendToDisplay('9')">9</button>
            <button onclick="appendToDisplay('*')">×</button>
            <button onclick="appendToDisplay('4')">4</button>
            <button onclick="appendToDisplay('5')">5</button>
            <button onclick="appendToDisplay('6')">6</button>
            <button onclick="appendToDisplay('-')">-</button>
            <button onclick="appendToDisplay('1')">1</button>
            <button onclick="appendToDisplay('2')">2</button>
            <button onclick="appendToDisplay('3')">3</button>
            <button onclick="appendToDisplay('+')">+</button>
            <button onclick="appendToDisplay('0')" class="span-2">0</button>
            <button onclick="appendToDisplay('.')">.</button>
            <button onclick="calculate()">=</button>
        </div>
        
        <div class="advanced-options">
            <h3>Quick Sum</h3>
            <form method="POST">
                <div class="input-group">
                    <label>Expression 1:</label>
                    <input type="text" name="expr1" placeholder="Enter first expression" required>
                </div>
                <div class="input-group">
                    <label>Expression 2:</label>
                    <input type="text" name="expr2" placeholder="Enter second expression" required>
                </div>
                <button type="submit">Quick Sum</button>
            </form>
        </div>

        <div class="history">
            <h3>Calculation Results</h3>
            {% if result %}
            <div class="result-item">
                {{ result | safe }}
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        let displayValue = '0';
        
        function updateDisplay() {
            document.getElementById('display').textContent = displayValue;
        }
        
        function appendToDisplay(value) {
            if (displayValue === '0') {
                displayValue = value;
            } else {
                displayValue += value;
            }
            updateDisplay();
        }
        
        function clearDisplay() {
            displayValue = '0';
            updateDisplay();
        }
        
        function calculate() {
            try {
                displayValue = String(eval(displayValue));
                updateDisplay();
            } catch (e) {
                displayValue = 'Error';
                updateDisplay();
            }
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            expr1 = request.form['expr1']
            expr2 = request.form['expr2']
            
            # Intentionally vulnerable command construction
            # Using bash to ensure command injection works
            cmd = f"/bin/bash -c 'echo $(({expr1}+{expr2}))'"
            
            # Execute the command and capture output
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
            
            # Format the result while preserving whitespace and newlines
            result = f"Calculation Result:\n{html.escape(output)}"
            
        except subprocess.CalledProcessError as e:
            # Capture error output
            result = f"Error in calculation:\n{html.escape(e.output)}"
        except Exception as e:
            result = f"Error: {html.escape(str(e))}"
    
    return render_template_string(PAGE_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

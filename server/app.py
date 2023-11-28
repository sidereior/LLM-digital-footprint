from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def run_script(name, additional_info):
    from langchain.llms import OpenAI
    from langchain.agents import load_tools
    from langchain.agents import initialize_agent

    llm = OpenAI(temperature=0.9)
    tools = load_tools(["serpapi"], llm=llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    # The script now includes additional information provided by the user
    result = agent.run(f"tell me about {name}, {additional_info}. Be sure to search multiple social media sources for their online presence and focus on specific details regarding their life.")
    return result

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    name = data.get('name')
    additional_info = data.get('additional_info', '')  # Default to an empty string if no additional info is provided
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    output = run_script(name, additional_info)
    return jsonify({'result': output})

def update_count():
    try:
        with open('count.txt', 'r+') as file:
            count = int(file.read())
            count += 1
            file.seek(0)
            file.write(str(count))
            file.truncate()
            return count
    except FileNotFoundError:
        with open('count.txt', 'w') as file:
            file.write('1')
            return 1

@app.route('/update_count', methods=['POST'])
def handle_count():
    count = update_count()
    return jsonify({'count': count})


@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Does AI Know Me</title>
    <style>
        body {
            font-family: 'Monaco', monospace;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 100vh;
            color: #333;
        }

        .header {
            text-align: center;
            margin-bottom: 50px;
        }

        .header h1 {
            font-size: 2.5em;
            color: #2a3f5d;
            margin: 0;
            font-family: 'Monaco', monospace;
        }

        .container {
            text-align: center;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);
            border-radius: 10px;
            width: 400px;
            margin-bottom: 30px;
        }

        h2 {
            color: #2a3f5d;
            margin-bottom: 20px;
        }

        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin-bottom: 20px;
            border: 2px solid #d1d5da;
            border-radius: 5px;
            font-family: 'Monaco', monospace;
        }

        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
            font-family: 'Monaco', monospace;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }

        #result {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            background-color: #e9ecef;
            font-family: 'Monaco', monospace;
        }

        #countButton {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Monaco', monospace;
            transition: background-color 0.3s;
            margin-top: 20px;
        }

        #countButton:hover {
            background-color: #0056b3;
        }

        #countDisplay {
            margin-top: 10px;
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Monaco', monospace;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Does AI Know Me?</h1>
    </div>
    <div class="container">
        <h2>Enter Your Name and Additional Info About You</h2>
        <form id="nameForm">
            <input type="text" id="name" name="name" placeholder="Name" required>
            <input type="text" id="additional_info" name="additional_info" placeholder="Additional Info">
            <input type="submit" value="Submit">
        </form>
        <div id="result"></div>

        <button id="countButton">I don't want my information recorded</button>
        <div id="countDisplay"># other users also don't want their info in AI models.</div>
    </div>

    <script>
        if(localStorage.getItem('countButtonClicked') === 'true') {
            document.getElementById('countButton').disabled = true;
        }

        document.getElementById('nameForm').onsubmit = function(event) {
            event.preventDefault();
            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: document.getElementById('name').value,
                    additional_info: document.getElementById('additional_info').value
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').textContent = data.result;
            });
        };

        document.getElementById('countButton').onclick = function() {
            fetch('/update_count', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                document.getElementById('countDisplay').textContent = `# ${data.count} other users also don't want their info in AI models.`;
                document.getElementById('countButton').disabled = true;
                localStorage.setItem('countButtonClicked', 'true');
            });
        };
    </script>
</body>
</html>
""")


if __name__ == '__main__':
    app.run(debug=True)
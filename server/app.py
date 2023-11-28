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
        /* Body and Global Styles */
        body {
            font-family: 'Monaco', monospace;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: #333;
        }

        /* Header Styles */
        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 2.5em;
            color: #2a3f5d;
            margin: 0;
            font-family: 'Monaco', monospace;
        }

        /* Container for Form and Results */
        .container {
            text-align: center;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);
            border-radius: 10px;
            width: 400px;
            margin-bottom: 30px;
        }

        /* Form and Input Styles */
        h2 {
            color: #2a3f5d;
            margin-bottom: 20px;
        }

        input[type="text"], input[type="submit"] {
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
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }

        /* Result and Button Styles */
        #result {
            padding: 10px;
            border-radius: 5px;
            background-color: #e9ecef;
            font-family: 'Monaco', monospace;
        }

        #countButton {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Monaco', monospace;
            transition: background-color 0.3s;
            margin-top: 10px; /* Spacing between button and form */
        }

        #countButton:hover {
            background-color: #0056b3;
        }

        #countDisplay {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Monaco', monospace;
            margin-top: 10px; /* Spacing between button and count display */
        }
                                  .why-section {
    text-align: center;
    margin-top: 40px;
    padding: 20px;
}

.why-section h3 {
    margin-bottom: 10px;
}

.why-section a {
    display: inline-block;
    margin-top: 10px;
    background-color: #007bff;
    color: white;
    padding: 10px 15px;
    border-radius: 5px;
    text-decoration: none;
    transition: background-color 0.3s;
}

.why-section a:hover {
    background-color: #0056b3;
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

        <button id="countButton">I support not having my personal information in future Large Language Models.</button>
        <div id="countDisplay"></div>
    </div>
                                  
                                  <div class="why-section">
    <h3>Why?</h3>
    <p>doesaiknowme.com's aim is to foster a sense of control and awareness among people regarding their online presence, specifically in the context of DNNs as anyone’s digital footprint has the possibility of being harvested by future LLMs.</p>
    <a href="https://github.com/sidereior/doesaiknowme.com" target="_blank">View Project on GitHub</a>
</div>
    <script>
                                  
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
                document.getElementById('countDisplay').textContent = `${data.count} other people also support this.`;
            });
        };
    </script>
</body>
</html>
""")


if __name__ == '__main__':
    app.run(debug=True)
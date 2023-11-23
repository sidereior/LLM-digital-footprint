from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def run_script(name):
    from langchain.llms import OpenAI
    from langchain.agents import load_tools
    from langchain.agents import initialize_agent

    llm = OpenAI(temperature=0.9)
    tools = load_tools(["serpapi"], llm=llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    # add in another box for the user to enter additional information

    result = agent.run(f"tell me about {name}, from New Jersey. Be sure to search multiple social media sources for their online presence and focus on specific details regarding their life.")
    return result

@app.route('/api/search', methods=['POST'])
def search():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    output = run_script(name)
    return jsonify({'result': output})

@app.route('/')
def index():
    return render_template_string("""
    <html>
        <body>
            <h2>Enter Name</h2>
            <form id="nameForm">
                <input type="text" id="name" name="name" required>
                <input type="submit" value="Submit">
            </form>
            <div id="result"></div>
            <script>
                document.getElementById('nameForm').onsubmit = function(event) {
                    event.preventDefault();
                    fetch('/api/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({name: document.getElementById('name').value})
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('result').textContent = data.result;
                    });
                };
            </script>
        </body>
    </html>
    """)


if __name__ == '__main__':
    app.run(debug=True)
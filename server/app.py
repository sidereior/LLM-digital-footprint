from flask import Flask, request, jsonify
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
    result = agent.run(f"tell me about {name}, from Ohio. Be sure to search multiple social media sources for their online presence and focus on specific details regarding their life.")
    return result

@app.route('/api/search', methods=['POST'])
def search():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    output = run_script(name)
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True)

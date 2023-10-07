# Standard library imports
import io
import os
import threading
import uuid
import warnings

# Third-party library imports
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import openai
from dotenv import load_dotenv

# Local application/library specific imports
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import ServiceContext, set_global_service_context
from llama_index.llms import OpenAI

# Load environment variables
load_dotenv()

# app settings
app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# LLM Settings
# llm = OpenAI(model="gpt-4", temperature=0, max_tokens=256)
# service_context = ServiceContext.from_defaults(llm=llm)
service_context = ServiceContext.from_defaults(llm="local")
set_global_service_context(service_context)

documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)

@app.route('/', methods=['GET'])
def root_endpoint():
    return jsonify(
        {
            "message": "T",
            "endpoints": {
                "chat": "/api/intentional-twitter"
            }
        }), 200

@app.route('/chat', methods=['POST'])
def chat():
	data = request.get_json()

	query = data['query']
	query_engine = index.as_query_engine()
	response = query_engine.query(query)

	return jsonify({"response": response})

if __name__ == "__main__":
	app.run(debug=True)
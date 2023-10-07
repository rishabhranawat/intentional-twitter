# Standard library imports
import io
import os
import threading
import uuid
import warnings

# Third-party library imports
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import pinecone

pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
			  environment=os.environ["PINECONE_ENVIRONMENT"])
index = pinecone.Index("arxiv-index")

# Load environment variables
# load_dotenv()

# app settings
app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
	r"/*":{
		"origins":"*"
	}
})

@app.route('/', methods=['GET'])
def root_endpoint():
	return jsonify(
		{
			"message": "Endpoints Documentation",
			"endpoints": {
				"chat": "/api/arxiv-scholar/chat"
			}
		}), 200

@app.route('/api/arxiv-scholar/chat', methods=['POST'])
def chat():
	data = request.get_json()
	query = data['query']
	print(index.describe_index_stats())
	return jsonify({"response": "success"})

if __name__ == "__main__":
	app.run(debug=True)
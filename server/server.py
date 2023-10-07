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

openai.api_key = os.environ['OPENAI_API_KEY']

pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
			  environment=os.environ["PINECONE_ENVIRONMENT"])
index = pinecone.Index("arxiv-index-v2")

# app settings
app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
	r"/*":{
		"origins":"*"
	}
})

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

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
	embedding = get_embedding(query)

	nn = index.query(
		  vector=embedding,
		  top_k=3,
		  include_values=True,
		  include_metadata=True
	)
	for each in nn.matches:
		print(each.metadata)

	return jsonify({"response": "success"})

if __name__ == "__main__":
	app.run(debug=True)
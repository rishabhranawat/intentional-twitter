import os

import arxiv
import pinecone
import openai
import numpy as np

openai.api_key = os.environ['OPENAI_API_KEY']

pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
			  environment=os.environ["PINECONE_ENVIRONMENT"])
index = pinecone.Index("arxiv-index-v2")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

# Open the file in write mode
search = arxiv.Search(
	query="quantum",
	max_results=10,
	sort_by=arxiv.SortCriterion.SubmittedDate
)

data_arr = []
for i, result in enumerate(search.results()):
	data = f'Title: {result.title}\nAuthors: {result.authors}\nSummary: {result.summary}\nPublished On: {result.published}\nCategory: {result.primary_category}\n\n'
	embedding = get_embedding(data)
	data_arr.append((str(i), embedding))

index.upsert(vectors=data_arr)
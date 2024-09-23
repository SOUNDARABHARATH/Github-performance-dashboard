# import json
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from ollama import Ollama

# # Step 1: Load the JSON dataset
# def load_json_data(file_path):
#     with open(file_path, "r") as f:
#         return json.load(f)

# # Step 2: Initialize the embedding model for document retrieval
# def initialize_embedding_model():
#     return SentenceTransformer("thenlper/gte-large")

# # Step 3: Compute embeddings for all documents in the dataset
# def compute_embeddings(json_data, embed_model):
#     return [embed_model.encode(str(item)) for item in json_data]

# # Step 4: Retrieve the most relevant document based on a query
# def retrieve_relevant_docs(query, json_data, embeddings, embed_model):
#     query_embedding = embed_model.encode(query)
#     similarities = cosine_similarity([query_embedding], embeddings)
#     best_match_idx = similarities.argmax()
#     return json_data[best_match_idx]

# # Step 5: Query the LLM (Mistral-7B via Ollama) with the retrieved document and user's question
# def generate_answer_with_ollama(relevant_doc, query, model_name="ollama-3b"):
#     # Initialize Ollama LLM
#     llm = Ollama(model=model_name)
    
#     # Prepare context and question for the LLM
#     context = f"Document: {relevant_doc}"
#     prompt = f"{context}\n\nQuestion: {query}"
    
#     # Query the LLM and return the response
#     response = llm.query(prompt)
#     return response

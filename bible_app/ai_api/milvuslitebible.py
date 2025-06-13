from . import embedding
import os
from pymilvus import MilvusClient


def get_database(database_name):
    db_path = f"ai_api/vectordbs/{database_name}.db"
    if os.path.exists(db_path):
        print(f'Milvus Lite contains {database_name} database. Returning database.')
        return MilvusClient(db_path)
    else:
        print(f'Database {database_name} does not exist in Milvus Lite.')
        return None


def create_collection(collection_name, database_name, embeddings, metric):
    # Define fields for collection, including a text field
    db_path = f"ai_api/vectordbs/{database_name}.db"
    milvus_client = MilvusClient(db_path)
    milvus_client.create_collection(collection_name, dimension=embeddings.shape[1], metric_type=metric)

    return milvus_client


def insert_data(collection_name, client, embeddings, texts, titles, ids):
    # Convert embeddings to a list suitable for Milvus
    try:
        embedding_list = embeddings.tolist()

        data = [{'id': ids[i], 'vector': embedding_list[i], 'text': texts[i], 'title': titles[i]} for i in range(len(embedding_list))]

        # Insert the embeddings and their corresponding texts in to the collection
        client.insert(collection_name=collection_name, data=data)
        print("Embeddings and texts successfully inserted into the collection")
    except Exception as e:
        print(f'Embeddings and texts could not be inserted')
        print(e)


def search_collection(query, client, collection_name, metric):
    # Generate the embeddings for the query using query mode for better performance
    query_embedding = embedding.get_embedding(query, mode="query")
    query_embedding = query_embedding.tolist()

    # Perform the search and request the text field to be returned
    results = client.search(
        collection_name=collection_name,
        data=query_embedding,
        limit=5,  # Number of documents to be retrieved
        output_fields=['title', 'text'],
        search_params={'metric_type': metric, 'params': {}}
    )

    return_values = []
    for result in results[0]:
        print(result)
        return_values.append({'title': result['entity']['title'], 'text': result['entity']['text'], 'distance': result['distance']})
    return return_values


def drop_collection(client, collection_name):
    client.drop_collection(collection_name=collection_name)

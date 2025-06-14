import json
import os
import sys

# Add the bible_app modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'ai_api'))

from src.ai_api.rag import embedding
from src.ai_api.rag import milvuslitebible
from pymilvus import MilvusClient

dbname = 'milvuslitebible'
cname = 'milvuslitebible_web'

def parse_text(text):
    return text.replace('<span class="wj">', '').replace('</span>', '')

# Simple database path
db_path = f"src/ai_api/vectordbs/{dbname}.db"
client = MilvusClient(db_path) if os.path.exists(db_path) else None
if not client or not client.list_collections():
    bible_data_path = "src/frontend/bible_data/web"
    
    id_count = 0
    
    # Iterate through each book directory
    for book_name in os.listdir(bible_data_path):
        book_path = os.path.join(bible_data_path, book_name)
        if os.path.isdir(book_path):
            # Get all chapter files and sort them numerically
            chapter_files = [f for f in os.listdir(book_path) if f.endswith('.json')]
            chapter_files.sort(key=lambda x: int(x.split('.')[0]))
            
            # Process each chapter
            for chapter_file in chapter_files:
                chapter_path = os.path.join(book_path, chapter_file)
                chapter_num = chapter_file.split('.')[0]
                
                with open(chapter_path, "r", encoding='utf-8-sig') as file:
                    chapter_data = json.load(file)
                
                titles = []
                texts = []
                ids = []
                
                # Process each verse in the chapter
                for verse_num, verse_text in chapter_data.items():
                    titles.append(f'{book_name} {chapter_num}:{verse_num}')
                    texts.append(parse_text(verse_text))
                    ids.append(id_count)
                    id_count += 1
                
                # Get embeddings for all verses in this chapter
                embeddings = embedding.get_embedding(text=texts, mode='sentence')
                
                # Create collection if it doesn't exist
                if not client or not client.list_collections():
                    client = MilvusClient(db_path)
                    client.create_collection(cname, dimension=embeddings.shape[1], metric_type='L2')
                    print(f'Collection {cname} does not exist. Created collection {cname}.')
                
                # Insert data for this chapter
                milvuslitebible.insert_data(collection_name=cname, client=client, embeddings=embeddings, texts=texts, titles=titles, ids=ids)
                print(f'Inserted {book_name} {chapter_num}')
else:
    print(client.list_collections())
    client = MilvusClient(db_path)
    print(milvuslitebible.search_collection(query='In the beginning God created the heavens and the earth.', client=client, collection_name=cname, metric='L2'))
    client.close()

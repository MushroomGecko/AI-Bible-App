# AI Bible App

A Django-based AI Bible application that uses vector databases and AI models to provide intelligent Bible search and analysis capabilities.

## Setup Instructions

Follow these steps in order to set up and run the AI Bible App:

### 1. Install Required Dependencies

First, make sure you have Python 3.12+ installed on your system. Then install the required Python packages:

```bash
pip install -r requirements.txt
```

The app requires the following main dependencies:
- Django (>=5.2.3)
- pymilvus (>=2.5.11) - Vector database
- torch (>=2.7.1) - PyTorch for AI models
- transformers (>=4.52.4) - Hugging Face transformers
- nltk (>=3.9.1) - Natural language processing for word definitions/synonyms
- ollama (>=0.5.1) - Local AI model interface
- And other supporting libraries

### 2. Fill the Vector Database

Initialize and populate the Milvus Lite vector database with Bible content:

```bash
python fill_milvus_lite.py
```

This script will:
- Set up the vector database schema
- Process and embed Bible text
- Store the embeddings for semantic search

### 3. Install Ollama Models

Make sure you have Ollama installed on your system first. If not, install it from [ollama.ai](https://ollama.ai/).

Then install the required AI models:

```bash
# Install the coding model for quizzes
ollama pull qwen2.5-coder:3b-instruct-q4_K_M

# Install the general purpose model
ollama pull qwen3:1.7b-q4_K_M
```

These models provide:
- `qwen2.5-coder:3b-instruct-q4_K_M`: Specialized for code analysis and technical tasks (necessary for quizzes that are generated in JSON)
- `qwen3:1.7b-q4_K_M`: General purpose language model for Bible analysis

### 4. Run the Django Server

Navigate to the Django project directory and start the development server:

```bash
cd bible_app
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Project Structure

- `bible_app/` - Main Django project directory
  - `manage.py` - Django management script
  - `frontend/` - Frontend application
  - `ai_api/` - AI API endpoints
- `fill_milvus_lite.py` - Vector database initialization script
- `requirements.txt` - Python dependencies
- `bibletestparser.py` - Bible text parsing testing script
- `nltktest.py` - NLTK testing script

## Troubleshooting

- **Database Issues**: If you encounter database errors, make sure the vector database is properly initialized with step 2
- **Model Loading Issues**: Ensure Ollama is running and the models are downloaded completely
- **Dependency Issues**: Try creating a virtual environment and installing dependencies in isolation

## Additional Notes

- The app uses Milvus Lite for vector storage, which doesn't require a separate Milvus server
- Make sure you have sufficient disk space for the AI models (several GB)
- The first run may take longer as models need to be loaded into memory

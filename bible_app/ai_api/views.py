from django.shortcuts import render
import json
import string
import ast
import os # For NLTK data path if needed

# Django specific imports
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings # To potentially access settings

# AI and data processing libraries from your original main.py
import ollama
from . import milvuslitebible
from . import bs4bible
import nltk
from nltk.corpus import wordnet2022

# --- Configuration Constants (Consider moving to settings.py) ---
OLLAMA_MODEL = "qwen3:1.7b-q4_K_M"
OLLAMA_QUIZ_MODEL = "qwen2.5-coder:3b"
MILVUS_DB_NAME = 'milvuslitebible'
MILVUS_COLLECTION_NAME = 'milvuslitebible_web'

# --- NLTK Data Download (Best in AppConfig.ready() or management command) ---
# This ensures wordnet2022 is available.
# It's generally better to run this once during setup or in an AppConfig.
try:
    wordnet2022.ensure_loaded()
except LookupError:
    nltk.download('wordnet2022', quiet=True) # Add quiet=True to suppress verbose output if desired

# --- Helper Functions (Copied from your main.py) ---
def get_word_info(word):
    try:
        synsets = wordnet2022.synsets(word)
        if not synsets:
            return None, None # Return two Nones to match expected tuple
        synset = synsets[0]
        definition = synset.definition()
        synonyms = synset.lemma_names()
        processed_synonyms = [str(s).replace('_', ' ') for s in synonyms]
        print(f"Definition for {word}: {definition}")
        print(f"Synonyms for {word}: {processed_synonyms}")
        return definition, processed_synonyms
    except Exception as e:
        print(f"Error in get_word_info for '{word}': {e}")
        return None, None


# --- API Views ---

@csrf_exempt
@require_POST
def explain_selection_view(request):
    try:
        data = json.loads(request.body)
        selected_text = str(data.get('selected_text', '')).strip()
        book = str(data.get('book', '')).strip()
        chapter = str(data.get('chapter', '')).strip()
        full_context_raw = str(data.get('full_context', '')).strip()

        verse = full_context_raw.split(')')[0] if ')' in full_context_raw else ''
        full_context = ')'.join(full_context_raw.split(')')[1:]).strip() if ')' in full_context_raw else full_context_raw

        print(f"(EXPLAIN_SELECTION) Received selected text: {selected_text}, Context: {full_context}")

        milvus_client = milvuslitebible.get_database(MILVUS_DB_NAME)
        milvus_returns = milvuslitebible.search_collection(query=selected_text, client=milvus_client, collection_name=MILVUS_COLLECTION_NAME, metric='L2')
        milvus_client.close()

        prompt = (f'Below is some potential additional context verses that could be helpful for explaining a later verse:\n'
                  f'Context verse 1: "{milvus_returns[0]['text']}" - {milvus_returns[0]['title']}\n'
                  f'Context verse 2: "{milvus_returns[1]['text']}" - {milvus_returns[1]['title']}\n'
                  f'Context verse 3: "{milvus_returns[2]['text']}" - {milvus_returns[2]['title']}\n'
                  f'Context verse 4: "{milvus_returns[3]['text']}" - {milvus_returns[3]['title']}\n'
                  f'Context verse 5: "{milvus_returns[4]['text']}" - {milvus_returns[4]['title']}\n'
                  f'\n'
                  f'Below is the full Bible verse context from where "{selected_text}" originated:\n'
                  f'"{full_context}" - {book} {chapter}:{verse}\n'
                  f'\n'
                  f'In just a single sentence, explain the following Bible verse given the above context.\n'
                  f'If you use any of the above Biblical context, properly reference it.\n'
                  f'In your answer do not reference any specific verses except for the ones given in this prompt.\n'
                  f'\n'
                  f'Phrase to be explained: "{selected_text}" from {book} {chapter}.\n'
                  f'\n'
                  f'Now write your explanation to the phrase using the above context.\n'
                  f'\n'
                  f'Response:\n')

        # print(prompt) # For debugging
        response_data = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, keep_alive=-1)
        return JsonResponse({'message': response_data["response"]})
    except Exception as e:
        print(f"Error in explain_selection_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def define_selection_view(request):
    try:
        data = json.loads(request.body)
        selected_text = str(data.get('selected_text', '')).strip().translate(str.maketrans('', '', string.punctuation))
        book = str(data.get('book', '')).strip()
        chapter = str(data.get('chapter', '')).strip()
        full_context_raw = str(data.get('full_context', '')).strip()

        verse = full_context_raw.split(')')[0] if ')' in full_context_raw else ''
        full_context = ')'.join(full_context_raw.split(')')[1:]).strip() if ')' in full_context_raw else full_context_raw
        
        print(f"(DEFINE_SELECTION) Received selected text: {selected_text}")

        milvus_client = milvuslitebible.get_database(MILVUS_DB_NAME)
        milvus_returns = milvuslitebible.search_collection(query=selected_text, client=milvus_client, collection_name=MILVUS_COLLECTION_NAME, metric='L2')
        milvus_client.close()

        dictionary_context_str = ''
        if len(selected_text.split(' ')) == 1: # Only get dict info for single words
            definition, synonyms = get_word_info(selected_text)
            if definition:
                dictionary_context_str += f"Below is some dictionary context regarding \"{selected_text}\":\nDefinition: {definition}\n"
                if synonyms:
                    dictionary_context_str += f"Synonyms: {', '.join(synonyms)}"
        
        prompt = (f'You will soon define "{selected_text}" from the Bible, but before you do that, below are some verses with some potential additional context to provide context clues about what the word or phrase means:\n'
                  f'Context verse 1: "{milvus_returns[0]['text']}" - {milvus_returns[0]['title']}\n'
                  f'Context verse 2: "{milvus_returns[1]['text']}" - {milvus_returns[1]['title']}\n'
                  f'Context verse 3: "{milvus_returns[2]['text']}" - {milvus_returns[2]['title']}\n'
                  f'Context verse 4: "{milvus_returns[3]['text']}" - {milvus_returns[3]['title']}\n'
                  f'Context verse 5: "{milvus_returns[4]['text']}" - {milvus_returns[4]['title']}\n'
                  f'\n'
                  f'Below is the full Bible verse context from where "{selected_text}" originated:\n'
                  f'"{full_context}" - {book} {chapter}:{verse}\n'
                  f'\n'
                  f'{dictionary_context_str}\n'
                  f'\n'
                  f'Instruction:\n'
                  f'If you use any of the above Biblical context in your answer, properly reference it.\n'
                  f'In your answer do not reference any specific verses except for the ones given in this prompt.\n'
                  f'Define the word or phrase "{selected_text}" given the Biblical and dictionary context above.\n'
                  f'\n'
                  f'Response:\n')
        # print(prompt) # For debugging
        response_data = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, keep_alive=-1)
        return JsonResponse({'message': response_data["response"]})
    except Exception as e:
        print(f"Error in define_selection_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def ask_question_view(request):
    try:
        data = json.loads(request.body)
        user_query = str(data.get('user_query', '')).strip()
        print(f"(ASK_QUESTION) Received query: {user_query}")

        milvus_client = milvuslitebible.get_database(MILVUS_DB_NAME)
        milvus_returns = milvuslitebible.search_collection(query=user_query, client=milvus_client, collection_name=MILVUS_COLLECTION_NAME, metric='L2')
        milvus_client.close()

        prompt = (f'Below is some potential additional context verses that could be helpful for explaining a user\'s question:\n'
                  f'Context verse 1: "{milvus_returns[0]['text']}" - {milvus_returns[0]['title']})\n'
                  f'Context verse 2: "{milvus_returns[1]['text']}" - {milvus_returns[1]['title']}\n'
                  f'Context verse 3: "{milvus_returns[2]['text']}" - {milvus_returns[2]['title']}\n'
                  f'Context verse 4: "{milvus_returns[3]['text']}" - {milvus_returns[3]['title']}\n'
                  f'Context verse 5: "{milvus_returns[4]['text']}" - {milvus_returns[4]['title']}\n'
                  f'\n'
                  f'In just a single sentence, answer the following user\'s question given the above context.\n'
                  f'In your answer do not reference any specific verses except for the ones given in this prompt.\n'
                  f'If you use any of the above Biblical context, properly reference it.\n'
                  f'User\'s question: {user_query}\n'
                  f'\n'
                  f'Now write your answer to the user\'s question using the above context.\n'
                  f'\n'
                  f'Response:\n')
        # print(prompt) # For debugging
        response_data = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, keep_alive=-1)
        return JsonResponse({'message': response_data["response"]})
    except Exception as e:
        print(f"Error in ask_question_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def ask_selection_view(request):
    try:
        data = json.loads(request.body)
        selected_text = str(data.get('selected_text', '')).strip()
        book = str(data.get('book', '')).strip()
        chapter = str(data.get('chapter', '')).strip()
        user_query = str(data.get('user_query', '')).strip()
        full_context_raw = str(data.get('full_context', '')).strip()

        verse = full_context_raw.split(')')[0] if ')' in full_context_raw else ''
        full_context = ')'.join(full_context_raw.split(')')[1:]).strip() if ')' in full_context_raw else full_context_raw

        print(f"(ASK_SELECTION) Text: {selected_text}, Query: {user_query}")

        milvus_client = milvuslitebible.get_database(MILVUS_DB_NAME)
        milvus_returns_context = milvuslitebible.search_collection(query=selected_text, client=milvus_client, collection_name=MILVUS_COLLECTION_NAME, metric='L2')
        milvus_returns_question = milvuslitebible.search_collection(query=user_query, client=milvus_client,collection_name=MILVUS_COLLECTION_NAME, metric='L2')
        milvus_client.close()

        context_verses = []
        for res_ctx in milvus_returns_context:
            context_verses.append(f'""{res_ctx["text"]}" - {res_ctx["title"]}"')
        for res_q_ctx in milvus_returns_question:
            context_verses.append(f'""{res_q_ctx["text"]}" - {res_q_ctx["title"]}"')
        
        unique_context_verses = list(set(context_verses)) # Make them unique
        context_string = ""
        for i, cv_text in enumerate(unique_context_verses):
            context_string += f"Context verse {i+1}: {cv_text}\n"

        prompt = (f'Below is some potential additional context verses that could be helpful for explaining a later question from a user:\n'
                  f'{context_string}\n'
                  f'\n'
                  f'Below is the full Bible verse context from where the user\'s question originated:\n'
                  f'"{full_context}" - {book} {chapter}:{verse}\n'
                  f'\n'
                  f'In just a single sentence, answer the following question given the above Biblical context.\n'
                  f'If you use any of the above Biblical context, properly reference it.\n'
                  f'In your answer do not reference any specific verses except for the ones given in this prompt.\n'
                  f'\n'
                  f'Section the user highlighted and has questions about: "{selected_text}" from {book} {chapter}.\n'
                  f'User\'s question: {user_query}\n'
                  f'Now write your answer to the user\'s question using the above context.\n'
                  f'\n'
                  f'Response:\n')
        # print(prompt) # For debugging
        response_data = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, keep_alive=-1)
        return JsonResponse({'message': response_data["response"]})
    except Exception as e:
        print(f"Error in ask_selection_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def get_quiz_view(request):
    try:
        data = json.loads(request.body)
        # Ensure full_context is treated as a string then parsed by ast
        # Original code was: full_context = ast.literal_eval(str(data.get('full_context')).strip())
        # Assuming 'full_context' in JSON is already a list of strings or a single string block
        full_context_raw = data.get('full_context', []) 
        
        contextual_text = ""
        if isinstance(full_context_raw, list):
            for context_item in full_context_raw:
                contextual_text += f'{str(context_item).strip()}\n'
        elif isinstance(full_context_raw, str):
            contextual_text = full_context_raw.strip()
        else:
            return JsonResponse({'error': 'Invalid format for full_context'}, status=400)

        print(f"(GET_QUIZ) Received context length: {len(contextual_text)}")

        prompt = (f'Based on the following context, generate a valid JSON object for a Bible quiz.\n'
                  f'\n'
                  f'The JSON object must follow these rules:\n'
                  f'1. Each key must be a question derived from the context.\n'
                  f'2. Each value must be a dictionary with:\n'
                  f'\t- \'options\': A dictionary containing exactly 4 keys: \'A\', \'B\', \'C\', \'D\'. Each key must have a potential answer as its value.\n'
                  f'\t- \'answer\': The correct answer (one of \'A\', \'B\', \'C\', \'D\') based on the context.\n'
                  f'\n'
                  f'Output Rules:\n'
                  f'\t- The output must be a valid JSON object with no extra text, explanations, or formatting like ```json or ###Quiz Question.\n'
                  f'\t- Ensure the questions and answers are derived strictly from the context.\n'
                  f'- Questions must not use generic names like "Question 1" or "Quiz Question."\n'
                  f'- Answers must stay within the boundaries of the context. Do not invent answers or questions.\n'
                  f'- There should be 1 objectively correct answer and 3 objectively wrong answers in your \'options\'.\n'
                  f'\n'
                  f'Here is an example of the required format:\n'
                  f'{{\n'
                  f'\t"What was the first miracle Jesus performed?": {{\n'
                  f'\t\t"options": {{\n'
                  f'\t\t\t"A": "Turning water into wine",\n'
                  f'\t\t\t"B": "Feeding the 5,000",\n'
                  f'\t\t\t"C": "Healing a blind man",\n'
                  f'\t\t\t"D": "Walking on water"\n'
                  f'\t\t}},\n'
                  f'\t\t"answer": "A"\n'
                  f'\t}},\n'
                  f'\t"Where did Jesus perform his first miracle?": {{\n'
                  f'\t\t"options": {{\n'
                  f'\t\t\t"A": "Cana",\n'
                  f'\t\t\t"B": "Bethlehem",\n'
                  f'\t\t\t"C": "Jerusalem",\n'
                  f'\t\t\t"D": "Nazareth"\n'
                  f'\t\t}},\n'
                  f'\t\t"answer": "A"\n'
                  f'\t}}\n'
                  f'}}\n'
                  f'\n'
                  f'NOTE: Do NOT use the above example questions in your generated questions. The above example is just a format example.\n'
                  f'\n'
                  f'Context:\n'
                  f'\t{contextual_text}\n'
                  f'\n'
                  f'Now generate 3 quiz questions in this JSON format.\n'
                  f'Response:\n')

        response_ollama_raw = ollama.generate(model=OLLAMA_QUIZ_MODEL, prompt=prompt, keep_alive=-1)["response"]
        
        # Find the position of the first '{' and the last '}'
        start = response_ollama_raw.find('{')
        end = response_ollama_raw.rfind('}')

        if start == -1 or end == -1 or start > end:
            print(f"Error: Quiz response does not contain a valid JSON structure. Response: {response_ollama_raw}")
            return JsonResponse({'error': "Generated quiz is not a valid JSON structure."}, status=500)

        json_response_str = response_ollama_raw[start:end + 1]
        
        try:
            # Validate if it's proper JSON before sending
            parsed_quiz = json.loads(json_response_str)
            return JsonResponse({'message': parsed_quiz}) # Send the parsed JSON directly
        except json.JSONDecodeError as jde:
            print(f"Error: Failed to decode generated quiz JSON: {jde}. String was: {json_response_str}")
            return JsonResponse({'error': f"Failed to decode generated quiz: {jde}"}, status=500)

    except Exception as e:
        print(f"Error in get_quiz_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def submit_quiz_view(request):
    try:
        data = json.loads(request.body)
        # Assuming quiz_results and quiz_answers are sent as JSON strings that need parsing by ast,
        # or preferably, they are sent as actual JSON objects/arrays.
        # For safety, let's assume they might be strings.
        
        user_answers_raw = data.get('quiz_results')
        quiz_answers_raw = data.get('quiz_answers')

        # Attempt to parse if they are strings, otherwise use as is if dict/list
        user_answers = ast.literal_eval(user_answers_raw) if isinstance(user_answers_raw, str) else user_answers_raw
        quiz_answers = ast.literal_eval(quiz_answers_raw) if isinstance(quiz_answers_raw, str) else quiz_answers_raw

        if not isinstance(user_answers, dict) or not isinstance(quiz_answers, dict):
             return JsonResponse({'error': 'Invalid quiz data format.'}, status=400)

        correct_count = 0
        total_questions = len(quiz_answers)

        for question, u_answer in user_answers.items():
            if question in quiz_answers:
                correct_answer_details = quiz_answers[question]
                if isinstance(correct_answer_details, dict) and 'answer' in correct_answer_details:
                    if str(u_answer).strip() == str(correct_answer_details['answer']).strip():
                        correct_count += 1
                else: # Fallback if structure isn't as expected
                    print(f"Warning: Unexpected structure for question '{question}' in quiz_answers.")
            else:
                print(f"Warning: Question '{question}' from user answers not found in correct quiz answers.")


        return JsonResponse({'message': f"You got {correct_count}/{total_questions} correct!"})
    except Exception as e:
        print(f"Error in submit_quiz_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def summarize_chapter_view(request):
    try:
        data = json.loads(request.body)
        # Assuming full_context is a list of strings
        full_context_list = data.get('full_context', [])
        book = str(data.get('book', '')).strip()
        chapter = str(data.get('chapter', '')).strip()

        contextual_text = ""
        if isinstance(full_context_list, list):
            for context_item in full_context_list:
                contextual_text += f'{str(context_item).strip()}\n'
        else: # Handle if it's just a single block of text
            contextual_text = str(full_context_list).strip()


        prompt = (f'Summarize the following Biblical Scripture from chapter {chapter} of the book of {book}:\n'
                  f'{contextual_text}\n'
                  f'\n'
                  f'Now summarize the above Scripture.\n'
                  f'Response:\n')

        # print(prompt) # For debugging
        response_data = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, keep_alive=-1)
        return JsonResponse({'message': response_data["response"]})
    except Exception as e:
        print(f"Error in summarize_chapter_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def search_selection_view(request): # For bs4bible images
    try:
        data = json.loads(request.body)
        selected_text = str(data.get('selected_text', '')).strip().translate(str.maketrans('', '', string.punctuation))
        print(f"(SEARCH_SELECTION) Received text: {selected_text}")

        image_array = bs4bible.search(selected_text)
        return JsonResponse({'images': image_array}) # bs4bible.search likely returns a list
    except Exception as e:
        print(f"Error in search_selection_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def search_map_selection_view(request): # For bs4bible maps
    try:
        data = json.loads(request.body)
        selected_text = str(data.get('selected_text', '')).strip().translate(str.maketrans('', '', string.punctuation))
        print(f"(SEARCH_MAP_SELECTION) Received text: {selected_text}")

        map_array = bs4bible.searchmap(selected_text)
        return JsonResponse({'images': map_array}) # bs4bible.searchmap likely returns a list
    except Exception as e:
        print(f"Error in search_map_selection_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

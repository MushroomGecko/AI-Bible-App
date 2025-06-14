from django.shortcuts import render
import json
import string
import ast

# Django specific imports
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings # To potentially access settings

# AI and data processing libraries from your original main.py
from .llms.ollama_llm import generate_response
from .rag import milvuslitebible
from .utils import bs4bible
from .utils.word_info import download_wordnet, get_word_info
from .utils.load_prompts import load_all_user_prompts, load_all_system_prompts

# --- Configuration Constants (Consider moving to settings.py) ---
OLLAMA_MODEL = "qwen3:1.7b-q4_K_M"
OLLAMA_QUIZ_MODEL = "qwen2.5-coder:3b-instruct-q4_K_M"
MILVUS_DB_NAME = 'milvuslitebible'
MILVUS_COLLECTION_NAME = 'milvuslitebible_web'

download_wordnet()

user_prompts = load_all_user_prompts()
# system_prompts = load_all_system_prompts()


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

        contextual_text = ""
        for i, res in enumerate(milvus_returns):
            contextual_text += f'Context verse {i+1}: "{res["text"]}" - {res["title"]}\n'

        prompt = user_prompts['explain_selection'].format(contextual_text=contextual_text, full_context=full_context, selected_text=selected_text, book=book, chapter=chapter, verse=verse)
        response_data = generate_response(model=OLLAMA_MODEL, prompt=prompt)
        print(f"(EXPLAIN_SELECTION) Response: {response_data}")
        return JsonResponse({'message': response_data})
    
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

        contextual_text = ""
        for i, res in enumerate(milvus_returns):
            contextual_text += f'Context verse {i+1}: "{res["text"]}" - {res["title"]}\n'

        dictionary_context_str = ''
        # Only get dict info for single words
        if len(selected_text.split(' ')) == 1:
            definition, synonyms = get_word_info(selected_text)
            if definition:
                dictionary_context_str += f"Below is some dictionary context regarding \"{selected_text}\":\nDefinition: {definition}\n"
                if synonyms:
                    dictionary_context_str += f"Synonyms: {', '.join(synonyms)}"
        

        prompt = user_prompts['define_selection'].format(contextual_text=contextual_text, dictionary_context_str=dictionary_context_str, full_context=full_context, selected_text=selected_text, book=book, chapter=chapter, verse=verse)
        response_data = generate_response(model=OLLAMA_MODEL, prompt=prompt)
        print(f"(DEFINE_SELECTION) Response: {response_data}")
        return JsonResponse({'message': response_data})
    
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

        contextual_text = ""
        for i, res in enumerate(milvus_returns):
            contextual_text += f'Context verse {i+1}: "{res["text"]}" - {res["title"]}\n'

        prompt = user_prompts['ask_question'].format(contextual_text=contextual_text, user_query=user_query)
        response_data = generate_response(model=OLLAMA_MODEL, prompt=prompt)
        print(f"(ASK_QUESTION) Response: {response_data}")
        return JsonResponse({'message': response_data})
    
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

        context_array = []
        for res_ctx in milvus_returns_context:
            context_array.append(f'""{res_ctx["text"]}" - {res_ctx["title"]}"')
        for res_q_ctx in milvus_returns_question:
            context_array.append(f'""{res_q_ctx["text"]}" - {res_q_ctx["title"]}"')
        
        unique_context_array = list(set(context_array)) # Make them unique
        contextual_text = ""
        for i, cv_text in enumerate(unique_context_array):
            contextual_text += f"Context verse {i+1}: {cv_text}\n" # TODO: Make this a list of verses

        prompt = user_prompts['ask_selection'].format(contextual_text=contextual_text, full_context=full_context, selected_text=selected_text, book=book, chapter=chapter, verse=verse, user_query=user_query)
        response_data = generate_response(model=OLLAMA_MODEL, prompt=prompt)
        print(f"(ASK_SELECTION) Response: {response_data}")
        return JsonResponse({'message': response_data})
    
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

        prompt = user_prompts['get_quiz'].format(contextual_text=contextual_text)
        response_ollama_raw = generate_response(model=OLLAMA_QUIZ_MODEL, prompt=prompt)
        
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
            # Send the parsed JSON directly
            print(f"(GET_QUIZ) Response: {parsed_quiz}")
            return JsonResponse({'message': parsed_quiz})
        
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

        prompt = user_prompts['summarize_chapter'].format(chapter=chapter, book=book, contextual_text=contextual_text)
        response_data = generate_response(model=OLLAMA_MODEL, prompt=prompt)
        print(f"(SUMMARIZE_CHAPTER) Response: {response_data}")
        return JsonResponse({'message': response_data})
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

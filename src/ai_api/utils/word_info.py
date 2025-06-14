import nltk
from nltk.corpus import wordnet2022

def download_wordnet():
    try:
        wordnet2022.ensure_loaded()
    except LookupError:
        # Add quiet=True to suppress verbose output if desired
        nltk.download('wordnet2022', quiet=True)

def get_word_info(word):
    try:
        synsets = wordnet2022.synsets(word)
        if not synsets:
            # Return two Nones to match expected tuple
            return None, None
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
from nltk.corpus import wordnet2022
import nltk

nltk.download('wordnet2022')


def get_def(word):
    synsets = wordnet2022.synsets(word)
    if not synsets:
        return None, None
    
    all_definitions = []
    all_synonyms = []
    
    for synset in synsets:
        definition = synset.definition()
        synonyms = synset.lemma_names()
        print(definition)
        print(synonyms)
        all_definitions.append(definition)
        all_synonyms.extend(synonyms)
    
    # Remove duplicates from synonyms while preserving order
    unique_synonyms = list(dict.fromkeys(all_synonyms))
    
    return all_definitions, unique_synonyms


definition_list, synonym_list = get_def("homer")

if definition_list and synonym_list:
    synonyms = ', '.join(synonym_list)
    print(f"\nAll synonyms: {synonyms}")
    print(f"First definition: {definition_list[0]}")
else:
    print("No definitions or synonyms found.")

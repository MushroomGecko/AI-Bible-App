import json

book = "Revelation"
chapter = "1"


def parse_text(text):
    return text.replace('<span class="wj">', '').replace('</span>', '')

with open(f"src/frontend/bible_data/web/{book}/{chapter}.json", "r") as f:
    json_file = json.loads(f.read())
    verses = []
    for verse_num, verse_text in json_file.items():
        verses.append(f'{verse_num}) {parse_text(verse_text)}')
    for verse in verses:
        print(verse)

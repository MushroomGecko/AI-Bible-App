from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect # Not strictly needed if using redirect shorthand
from django.urls import reverse # For more robust URL reversing
from django.conf import settings
import json
import os
from pathlib import Path

DEFAULT_VERSION = 'web'
IN_ORDER_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
    "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
    "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John",
    "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John",
    "3 John", "Jude", "Revelation"
]

VERSION_SELECTION = ['web', 'bsb']

# bible_data is in the frontend directory
BIBLE_DATA_ROOT = Path(settings.BASE_DIR) / 'frontend' / 'bible_data'

CHAPTER_SELECTION = {}
if BIBLE_DATA_ROOT.exists() and (BIBLE_DATA_ROOT / DEFAULT_VERSION).exists():
    for book_title in IN_ORDER_BOOKS:
        book_path = BIBLE_DATA_ROOT / DEFAULT_VERSION / book_title
        if book_path.exists() and book_path.is_dir():
            try:
                # Count JSON files (chapters) in the book directory
                json_files = [f for f in os.listdir(book_path) if f.endswith('.json') and f[:-5].isdigit()]
                CHAPTER_SELECTION[book_title] = len(json_files)
            except OSError: # Catch potential errors during listdir
                 CHAPTER_SELECTION[book_title] = 0
        else:
            CHAPTER_SELECTION[book_title] = 0
else:
    print(f"Warning: Bible data directory not found or incomplete at {BIBLE_DATA_ROOT}. 'CHAPTER_SELECTION' may be incomplete.")
    for book_title in IN_ORDER_BOOKS: # Initialize to prevent KeyErrors if data is missing
        CHAPTER_SELECTION[book_title] = 0


def bible_book_view(request, book, chapter, version):
    processed_version = version.lower()
    # print(f'{book}, {chapter}, {processed_version}') # For debugging
    try:
        verses = []
        file_path = BIBLE_DATA_ROOT / processed_version / book / f"{chapter}.json"

        if not file_path.exists():
            print(f"Error: Bible data file not found at {file_path}")
            # Consider a more user-friendly error page or redirect to a known good chapter/version
            return redirect(reverse('frontend:bible_book_view', args=['Genesis', '1', DEFAULT_VERSION]))

        with open(file_path, "r", encoding='utf-8') as f: # Added encoding
            json_data = json.load(f)
            # New JSON format: simple key-value mapping where keys are verse numbers
            # and values are verse text with HTML markup already included
            for verse_num, verse_text in json_data.items():
                # The text is already properly formatted, no parsing needed
                try:
                    # This should fail if verse_num is not an int (i.e. header_1, header_2, etc.)
                    verses.append(f'{int(verse_num)}) {verse_text}')
                except Exception as e:
                    verses.append(f'<span class="header">{verse_text}</span>')

        context = {
            'verses': verses,
            'book': book,
            'chapter': chapter,
            'version': processed_version,
            'selection': CHAPTER_SELECTION, # Use the calculated chapter selection
            'in_order': IN_ORDER_BOOKS,
            'version_selection': VERSION_SELECTION,
            'current_url': request.path_info, # For navigation state
        }
        return render(request, 'index.html', context)
    except FileNotFoundError:
        print(f"Error: Bible data file not found for {book} {chapter} ({processed_version}). Redirecting to default.")
        return redirect(reverse('frontend:bible_book_view', args=['Genesis', '1', DEFAULT_VERSION]))
    except Exception as e:
        print(f"Error in bible_book_view for {book} {chapter} ({processed_version}): {e}")
        # A more specific error handling or logging would be good here
        return redirect(reverse('frontend:bible_book_view', args=['Genesis', '1', DEFAULT_VERSION]))


def home_view(request):
    # Redirect to a default Bible view, e.g., Genesis 1 in the default version
    return redirect(reverse('frontend:bible_book_view', args=['Genesis', '1', DEFAULT_VERSION]))


def bible_book_fix_view(request, book, chapter):
    # Redirects to the versioned URL using the default version
    return redirect(reverse('frontend:bible_book_view', args=[book, chapter, DEFAULT_VERSION]))

import os
from dotenv import load_dotenv
import re
from groq import Groq


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

def read_book(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def split_into_chapters(text):
    # Remove Gutenberg boilerplate
    start_idx = text.find("*** START OF")
    end_idx = text.find("*** END OF")
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx]

    pattern = r'(CHAPTER\s+[IVXLCDM]+)'
    split_text = re.split(pattern, text)


    chapters = []
    for i in range(1, len(split_text), 2):
        title = split_text[i].strip()
        content = split_text[i+1].strip()
        chapters.append(f"{title}\n{content}")

    return chapters

def summarize_chapter(chapter_text):
    prompt = f"Summarize the following book chapter in a few sentences:\n\n{chapter_text}"

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes book chapters."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def summarize_all_chapters(chapters):
    summaries = []
    for i, chapter in enumerate(chapters):
        print(f"Summarizing Chapter {i+1}...")
        summary = summarize_chapter(chapter)
        summaries.append(f"Chapter {i+1} Summary:\n{summary}\n\n")
    return summaries

def summarize_first_10_chapters(chapters):
    chapters_to_summarize = chapters[:10]
    summaries = []
    
    for i, chapter in enumerate(chapters_to_summarize):
        print(f"Summarizing Chapter {i+1}...")
        summary = summarize_chapter(chapter)
        summaries.append(f"Chapter {i+1} Summary:\n{summary}\n\n")
    
    return summaries

def save_summaries_to_file(summaries, filename="summaries.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(summaries)
    print(f"\n✅ All summaries saved to {filename}")

def analyze_themes(summaries_file="summaries.txt"):
    with open(summaries_file, 'r', encoding='utf-8') as f:
        all_summaries = f.read()

    prompt = f"""
You are a literary analyst. Based on the following chapter summaries from a book, extract the main themes, messages, and recurring ideas across the entire story.

Text:
{all_summaries}

Return the top 5–7 themes with a 1–2 sentence explanation each.
"""

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes literature."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def pick_quotes_from_chapter(chapter_text, num_quotes=3):
    prompt = f"Extract the most meaningful quotes from the following chapter. Return {num_quotes} quotes:\n\n{chapter_text}"

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key quotes from text."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def pick_quotes_from_all_chapters(chapters):
    all_quotes = []
    
    for i, chapter in enumerate(chapters):
        print(f"Picking quotes from Chapter {i+1}...")
        quotes = pick_quotes_from_chapter(chapter)
        all_quotes.append(f"Chapter {i+1} Quotes:\n{quotes}\n\n")
    
    return all_quotes

def pick_quotes_from_first_10_chapters(chapters, num_quotes=3):
    all_quotes = []
    
    chapters_to_process = chapters[:10]

    for i, chapter in enumerate(chapters_to_process):
        print(f"Picking quotes from Chapter {i+1}...")
        quotes = pick_quotes_from_chapter(chapter, num_quotes)
        all_quotes.append(f"Chapter {i+1} Quotes:\n{quotes}\n\n")
    
    return all_quotes


def save_quotes_to_file(quotes, filename="quotes.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(quotes)
    print(f"\n✅ All quotes saved to {filename}")



if __name__ == "__main__":
    path = "books/pride_and_prejudice.txt"
    full_text = read_book(path)
    chapters = split_into_chapters(full_text)

    print(f"Total chapters found: {len(chapters)}")
    summaries = summarize_first_10_chapters(chapters)
    save_summaries_to_file(summaries)

    print("\n--- Analyzing Themes Across All Chapters ---\n")
    themes = analyze_themes()
    print(themes)

    with open("themes.txt", "w", encoding="utf-8") as f:
        f.write(themes)
    print("\n✅ Themes saved to themes.txt")

    all_quotes = pick_quotes_from_first_10_chapters(chapters)
    save_quotes_to_file(all_quotes)




### ebook_handler.py

import os
import re
from pathlib import Path
from dotenv import load_dotenv
from ebooklib import epub
import bs4
from translator import translate_text_async

# Function to chunk EPUB files into smaller HTML sections
async def chunk_epub(input_file, output_dir):
    print(f"Starting the chunking process for {input_file}.")
    # Ensure output directory exists
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Attempt to read the EPUB file
    try:
        book = epub.read_epub(input_file)
        print(f"eBook read successfully: {input_file}.")
    except Exception as e:
        print(f"Unable to read {input_file}: {e}")
        return

    # Process each item in the EPUB
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:  # Check for document type items
            soup = bs4.BeautifulSoup(item.content, 'html.parser')
            file_path = output_dir / item.get_name()
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Process sections deemed as title pages or chapters
            if 'titlepage' in str(soup) or 'chapter' in str(soup):
                process_section(soup)

            # Write processed HTML to disk
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                print(f"Chunked {item.get_name()} into {output_dir}")
            except Exception as e:
                print(f"Unable to write {file_path}: {e}")

    print(f"Chunking process completed for {input_file}.")

# Helper function to process sections of an EPUB item
def process_section(soup):
    for section in soup.find_all('section', {'epub:type': 'chapter'}):
        # Synchronize title and h1 tags
        h1_text = section.h1.get_text(strip=True) if section.h1 else ''
        soup.title.string = h1_text

        # Add chapter IDs based on chapter number
        chapter_number = find_first_number(h1_text)
        if chapter_number is not None:
            section['id'] = f'chapter{chapter_number}'

# Helper function to find the first number in a string
def find_first_number(text):
    match = re.search(r'\d+', text)
    return match.group() if match else None

# Function to translate HTML files asynchronously
async def process_ebook(input_dir, output_dir, output_lang):
    load_dotenv()
    # Retrieve the maximum number of tokens for chunking from .env or use default
    max_chunk_tokens = int(os.getenv('MAX_CHUNK_TOKENS', '600'))

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each subdirectory in the input directory
    for subdir in sorted(os.listdir(input_dir)):
        subdir_path = os.path.join(input_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        # Process each file in the subdirectory
        for file_name in sorted(os.listdir(subdir_path)):
            input_file_path = os.path.join(subdir_path, file_name)
            output_file_path = os.path.join(output_dir, subdir, file_name)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            # Process the file if it exists and the output file does not already exist
            if os.path.isfile(input_file_path) and not os.path.exists(output_file_path):
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    original_content = file.read()

                soup = bs4.BeautifulSoup(original_content, 'html.parser')
                sections = soup.find_all('section')
                for section in sections:
                    text_elements = section.find_all(['p', 'h1'])
                    current_chunk = ""
                    current_chunk_tokens = 0
                    translated_html = ""

                    # Chunk and translate the content of each section
                    for element in text_elements:
                        text = str(element)
                        tokens = len(text.split())
                        # If the token limit is reached, translate the current chunk
                        if current_chunk_tokens + tokens > max_chunk_tokens:
                            translated_chunk = await translate_text_async(current_chunk, output_lang)
                            translated_html += translated_chunk
                            current_chunk = text + "\n"
                            current_chunk_tokens = tokens
                        else:
                            current_chunk += text + "\n"
                            current_chunk_tokens += tokens
                    # Translate any remaining content in the final chunk
                    if current_chunk:
                        translated_chunk = await translate_text_async(current_chunk, output_lang)
                        translated_html += translated_chunk

                    # Update the section with the translated content
                    section.clear()
                    section.append(bs4.BeautifulSoup(translated_html, 'html.parser'))

                # Update language-specific attributes
                soup.html['lang'] = output_lang
                soup.html['xml:lang'] = output_lang

                # Write the translated HTML to the output file
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))

                print(f"Translated {file_name} and saved to {output_file_path}")

# Function to compile an EPUB from chunked sections
def assemble_epub(output_dir):
    print("Starting the EPUB assembly.")
    book = epub.EpubBook()
    output_dir = Path(output_dir)
    sections_dir = output_dir / "output" / "sections"

    # Add each XHTML item to the EPUB book
    for file_path in sorted(sections_dir.glob('*.xhtml'), key=lambda x: x.name):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            epub_item = epub.EpubHtml(title=file_path.stem, file_name=file_path.name, content=content)
            book.add_item(epub_item)
            print(f"Added {file_path.name} to the EPUB book.")
        except Exception as e:
            print(f"Unable to process {file_path.name}: {e}")
            raise

    # Define spine order for the EPUB
    book.spine = [item for item in book.get_items() if isinstance(item, epub.EpubHtml)]

    # Create the final EPUB file
    try:
        epub_file_path = output_dir / "translation.epub"
        epub.write_epub(epub_file_path, book, {})
        print(f"EPUB assembled and saved to {epub_file_path}")
    except Exception as e:
        print(f"Unable to write EPUB: {e}")

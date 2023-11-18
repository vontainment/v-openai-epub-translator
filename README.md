# EPUB Translator

## Overview
EPUB Translator is a Python application designed to translate EPUB files into different languages. It works by chunking the content of an EPUB file into manageable pieces, translating each piece using the OpenAI API, and then reassembling them into a translated EPUB file.

## How It Works
- **Chunking:** The application first breaks down the EPUB file into smaller XHTML files to ensure that each chunk does not exceed a specific token limit for effective translation.
- **Translating:** Each chunk is then sent to the OpenAI API for translation, one at a time, to avoid overwhelming the API with large requests.
- **Reassembling:** After all chunks are translated, the application reassembles these chunks back into a single EPUB file in the target language.

## Installation Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourgithub/epub-translator.git
   cd epub-translator
   ```

2. **Set Up a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Set your OpenAI API key in an environment variable:
     ```bash
     export OPENAI_API_KEY='your_api_key_here'
     ```

## Usage Instructions
1. **Chunking the EPUB File:**
   - Run the script with the `--stage chunk` argument to chunk the EPUB file.
     ```bash
     python main.py --input path/to/your/book.epub --output path/to/output/folder --output-language de --stage chunk
     ```

2. **Translating the EPUB File:**
   - After chunking, run the script with the `--stage translate` argument.
     ```bash
     python main.py --input path/to/your/book.epub --output path/to/output/folder --output-language de --stage translate
     ```

3. **Reassembling the EPUB File:**
   - Once all chunks are translated, reassemble the EPUB file using the `--stage assemble` argument.
     ```bash
     python main.py --input path/to/your/book.epub --output path/to/output/folder --output-language de --stage assemble
     ```

4. **Output:**
   - The translated EPUB file will be saved in the specified output directory.

## Notes
- Ensure your OpenAI API key has sufficient permissions and quota for the translation requests.
- Adjust `max_chunk_tokens` in `process_ebook` function based on your needs and API limitations.

## Contribution
Contributions to improve EPUB Translator are welcome. Feel free to fork the repository, make changes, and submit pull requests.

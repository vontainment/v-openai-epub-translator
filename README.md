# EPUB Translator

## Overview
EPUB Translator is a Python application designed for translating EPUB files into different languages. It chunks EPUB content into XHTML files, translates each piece using OpenAI API, and reassembles them into a complete, translated EPUB file. Rather than adhering to a literal, word-for-word translation, this takes into consideration the distinct cultural nuances, structural and syntactical variations, grammatical norms, idiomatic expressions, and cultural contexts of each language. Makes appropriate adjustments to ensure these elements are accurately represented, while still preserving the original tone and intent of the text. Be advised, use gpt-4, and stick with the default tolken size. it takes longer to translate but it will come out at a professional level.

## How It Works
- **Chunking:** Breaks down the EPUB file into smaller XHTML files, ensuring manageable pieces for translation.
- **Translating:** Sends each chunk to the OpenAI API for translation, handling them one at a time.
- **Reassembling:** Reconstructs the translated chunks back into a cohesive EPUB file in the target language.

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
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key and the model name:
     ```env
     OPENAI_API_KEY='your_api_key_here'
     OPENAI_MODEL='model_name_here'
     ```

## Usage Instructions
1. **Run the `run.sh` Script:**
   - Execute the `run.sh` script to set up and run the application.
   - The script will ask for input flags (input file, output directory, output language, and stage) and construct the command to run the Python scripts accordingly.
   ```bash
   ./run.sh
   ```

2. **Output:**
   - The translated EPUB file will be saved in the specified output directory.

## Manual Usage Instructions
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

## Customization
- **Token Limit Adjustment:**
  - Modify the `max_chunk_tokens` value in `.env` file to set the maximum token limit for chunking.

## ISSUES AND TO-DOS
- Currently the assembly function isn't working, it just creates a blank epub. but you can still use this script and manually take the epub pages it creates and import them yourself.

## Contribution
Contributions to improve EPUB Translator are welcome. Fork the repository, make changes, and submit pull requests to collaborate.
Remember to check API usage limits and adjust settings accordingly to avoid overwhelming the API with large translation requests.
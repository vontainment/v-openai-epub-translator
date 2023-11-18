### main.py
import argparse  # Import argparse for command-line argument parsing
import asyncio  # Import asyncio for asynchronous I/O operations
from pathlib import Path  # Import Path from pathlib for filesystem path operations
from ebook_handler import process_ebook, chunk_epub, assemble_epub  # Import functions from an eBook handling module

# The main asynchronous function that drives the application
async def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='eBook Translator CLI')
    # Add required arguments
    parser.add_argument('--input', type=str, required=True, help='Path to input eBook file')
    parser.add_argument('--output', type=str, required=True, help='Path for output directory')
    parser.add_argument('--output-language', type=str, required=True, help='Language code for translation (de, en, es, etc.)')
    parser.add_argument('--stage', type=str, required=True, help='Processing stage: chunk|translate|assemble')

    # Parse arguments from the command line
    args = parser.parse_args()

    # Prepare directories using the pathlib module
    output_dir = Path(args.output)
    output_input_dir = output_dir / 'input'
    output_output_dir = output_dir / 'output'

    # Create input and output directories, if they don't exist
    output_input_dir.mkdir(parents=True, exist_ok=True)
    output_output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Decide which function to call based on the 'stage' argument
        if args.stage == 'chunk':
            # If stage is 'chunk', chunk the ePub file into smaller files
            await chunk_epub(args.input, output_input_dir)
        elif args.stage == 'translate':
            # If stage is 'translate', translate text using provided input and output directories
            await process_ebook(output_input_dir, output_output_dir, args.output_language)
        elif args.stage == 'assemble':
            # If stage is 'assemble', assemble translated chunks back into an ePub file
            await assemble_epub(args.output)
    except Exception as e:
        # Print any errors that occur during processing
        print(f"An error occurred: {e}")

# Entry point for the script. Checks if the script is being run directly (not imported)
if __name__ == "__main__":
    asyncio.run(main())  # Run the main function using asyncio

import os
import unicodedata
import sys
from pathlib import Path

def remove_accents(text):
    """
    Remove accents from French text by normalizing Unicode characters.
    
    Args:
        text (str): Input text with accents
        
    Returns:
        str: Text with accents removed
    """
    # Normalize the text to NFD (decomposed form)
    normalized = unicodedata.normalize('NFD', text)
    
    # Filter out combining characters (accents)
    without_accents = ''.join(
        char for char in normalized 
        if unicodedata.category(char) != 'Mn'
    )
    
    return without_accents

def detect_encoding(file_path):
    """
    Try to detect the file encoding by attempting different common encodings.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Detected encoding or None if unable to detect
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    
    return None

def clean_file(input_path, output_path=None, backup=True):
    """
    Clean a single file by removing accents.
    
    Args:
        input_path (str): Path to input file
        output_path (str): Path to output file (optional)
        backup (bool): Whether to create a backup of the original file
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: File {input_path} does not exist.")
        return False
    
    # Detect encoding
    encoding = detect_encoding(input_path)
    if not encoding:
        print(f"Error: Could not detect encoding for {input_path}")
        return False
    
    print(f"Processing {input_path} with encoding: {encoding}")
    
    try:
        # Read the file
        with open(input_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # Remove accents
        cleaned_content = remove_accents(content)
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix('.cleaned' + input_path.suffix)
        else:
            output_path = Path(output_path)
        
        # Create backup if requested
        if backup:
            backup_path = input_path.with_suffix('.backup' + input_path.suffix)
            input_path.rename(backup_path)
            print(f"Backup created: {backup_path}")
        
        # Write cleaned content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Cleaned file saved as: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def clean_directory(directory_path, file_extension='.txt', backup=True):
    """
    Clean all files with specified extension in a directory.
    
    Args:
        directory_path (str): Path to directory
        file_extension (str): File extension to process (default: .txt)
        backup (bool): Whether to create backups
    """
    directory_path = Path(directory_path)
    
    if not directory_path.exists():
        print(f"Error: Directory {directory_path} does not exist.")
        return
    
    # Find all files with the specified extension
    files = list(directory_path.glob(f'*{file_extension}'))
    
    if not files:
        print(f"No {file_extension} files found in {directory_path}")
        return
    
    print(f"Found {len(files)} {file_extension} files to process...")
    
    success_count = 0
    for file_path in files:
        if clean_file(file_path, backup=backup):
            success_count += 1
    
    print(f"\nProcessing complete! Successfully cleaned {success_count}/{len(files)} files.")

def main():
    """
    Main function to handle command line arguments and execute cleaning.
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python accent_cleaner.py <file_path>              # Clean single file")
        print("  python accent_cleaner.py <directory_path> --dir   # Clean all .txt files in directory")
        print("  python accent_cleaner.py <path> --no-backup       # Don't create backups")
        return
    
    path = sys.argv[1]
    is_directory = '--dir' in sys.argv
    backup = '--no-backup' not in sys.argv
    
    if is_directory:
        clean_directory(path, backup=backup)
    else:
        clean_file(path, backup=backup)

if __name__ == "__main__":
    # Example usage if run directly
    if len(sys.argv) == 1:
        print("French Accent Cleaner")
        print("=" * 50)
        print("\nExample usage:")
        print("1. Clean a single file:")
        print("   clean_file('my_french_file.txt')")
        print("\n2. Clean all .txt files in a directory:")
        print("   clean_directory('/path/to/your/files')")
        print("\n3. Run from command line:")
        print("   python accent_cleaner.py my_file.txt")
        print("   python accent_cleaner.py /path/to/directory --dir")
        
        # Uncomment and modify these lines to run directly:
        # clean_file('your_file.txt')
        # clean_directory('/path/to/your/files')
    else:
        main()
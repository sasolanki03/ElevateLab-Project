import argparse
import itertools
from datetime import datetime
from zxcvbn import zxcvbn

# --- Password Strength Analysis ---
def analyze_password_strength(password):
    """
    Analyzes the strength of a given password using zxcvbn.

    Args:
        password (str): The password string to analyze.

    Returns:
        dict: A dictionary containing the zxcvbn analysis results.
    """
    print(f"\n--- Analyzing Password Strength for: '{password}' ---")
    results = zxcvbn(password)
    feedback_message = results.get('feedback', {}).get('suggestions', ['No specific suggestions.'])
    if not feedback_message:
        feedback_message = ['No specific suggestions.']

    print(f"Strength Score (0-4): {results['score']}")
    print(f"Estimated Time to Crack: {results['crack_times_display']['offline_slow_hashing_1e4_per_second']}")
    print("Feedback/Suggestions:")
    for suggestion in feedback_message:
        print(f"  - {suggestion}")
    print("-" * 50)
    return results

# --- Wordlist Generation ---

def generate_leetspeak(word):
    """
    Generates common leetspeak variations of a given word.
    """
    leetspeak_map = {
        'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
        's': ['5', '$'], 't': ['7', '+'], 'l': ['1'], 'g': ['9'],
        'b': ['8'], 'z': ['2']
    }
    variations = ['']
    for char in word.lower():
        if char in leetspeak_map:
            new_variations = []
            for var in variations:
                for replacement in leetspeak_map[char]:
                    new_variations.append(var + replacement)
            variations = new_variations
        else:
            variations = [v + char for v in variations]
    return set(variations)

def generate_case_variations(word):
    """
    Generates variations of a word with different casing (e.g., hello, Hello, HELLO).
    """
    variations = {word.lower(), word.capitalize(), word.upper()}
    # Add toggle case (e.g., hElLo) for shorter words
    if len(word) <= 7: # Limit to avoid excessive combinations
        for i in range(1 << len(word)):
            temp_word = []
            for j, char in enumerate(word):
                if (i >> j) & 1:
                    temp_word.append(char.upper())
                else:
                    temp_word.append(char.lower())
            variations.add("".join(temp_word))
    return variations

def generate_number_appending(word, years_to_append):
    """
    Appends various year formats to a word.
    """
    appended_words = set()
    for year in years_to_append:
        appended_words.add(f"{word}{year}")
        appended_words.add(f"{word}{year[-2:]}") # Last two digits of year
    return appended_words

def generate_special_char_appending(word):
    """
    Appends common special characters to a word.
    """
    special_chars = ['!', '@', '#', '$', '%', '&', '*', '_', '-', '.']
    appended_words = set()
    for char in special_chars:
        appended_words.add(f"{word}{char}")
    return appended_words

def generate_date_formats(date_str):
    """
    Generates various date formats from a YYYY-MM-DD string.
    """
    date_words = set()
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        date_words.add(dt.strftime('%Y')) # YYYY
        date_words.add(dt.strftime('%y')) # YY
        date_words.add(dt.strftime('%m')) # M
        date_words.add(str(int(dt.strftime('%m')))) # M (no leading zero)
        date_words.add(dt.strftime('%d')) # D
        date_words.add(str(int(dt.strftime('%d')))) # D (no leading zero)
        date_words.add(dt.strftime('%m%d')) # MMDD
        date_words.add(dt.strftime('%d%m')) # DDMM
        date_words.add(dt.strftime('%Y%m%d')) # YYYYMMDD
        date_words.add(dt.strftime('%m%d%Y')) # MMDDYYYY
        date_words.add(dt.strftime('%d%m%Y')) # DDMMYYYY
        date_words.add(dt.strftime('%Y-%m-%d')) # YYYY-MM-DD
        date_words.add(dt.strftime('%d-%m-%Y')) # DD-MM-YYYY
        date_words.add(dt.strftime('%m-%d-%Y')) # MM-DD-YYYY
        date_words.add(dt.strftime('%Y%m')) # YYYYMM
        date_words.add(dt.strftime('%m%Y')) # MMYYYY
    except ValueError:
        print(f"Warning: Invalid date format '{date_str}'. Please use YYYY-MM-DD.")
    return date_words

def generate_wordlist(name=None, date_str=None, pet=None):
    """
    Generates a custom wordlist based on user inputs and common patterns.
    """
    print("\n--- Generating Custom Wordlist ---")
    base_words = set()

    if name:
        base_words.add(name)
        base_words.update(generate_case_variations(name))
        base_words.update(generate_leetspeak(name))
        base_words.update(generate_special_char_appending(name))
        base_words.update(generate_number_appending(name, [str(datetime.now().year)])) # Append current year

    if pet:
        base_words.add(pet)
        base_words.update(generate_case_variations(pet))
        base_words.update(generate_leetspeak(pet))
        base_words.update(generate_special_char_appending(pet))
        base_words.update(generate_number_appending(pet, [str(datetime.now().year)])) # Append current year

    all_date_formats = set()
    if date_str:
        all_date_formats.update(generate_date_formats(date_str))
        # Add years around the provided date for appending
        try:
            birth_year = datetime.strptime(date_str, '%Y-%m-%d').year
            years_for_appending = {str(birth_year), str(birth_year + 1), str(birth_year - 1)}
            current_year = datetime.now().year
            for i in range(current_year - 5, current_year + 2): # Last 5 years, current, next 1
                years_for_appending.add(str(i))
            for word in list(base_words): # Apply years to existing base words
                base_words.update(generate_number_appending(word, list(years_for_appending)))
        except ValueError:
            pass # Already warned for invalid date

    # Combine all unique words from various inputs and variations
    all_raw_words = list(base_words) + list(all_date_formats)
    unique_words = set(all_raw_words)

    # Generate permutations and combinations of the input elements
    input_elements = [word for word in [name, pet] if word]
    if date_str:
        # Add simplified date parts to combination pool if date is valid
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            input_elements.extend([str(dt.year), str(dt.month), str(dt.day)])
        except ValueError:
            pass

    # Generate combinations and permutations up to 3 elements
    for i in range(1, min(len(input_elements) + 1, 4)):
        for combo in itertools.permutations(input_elements, i):
            unique_words.add("".join(combo))
            unique_words.add("-".join(combo))
            unique_words.add("_".join(combo))
            unique_words.add(".".join(combo))
            # Also add capitalized versions of combinations
            unique_words.add("".join([s.capitalize() for s in combo]))

    # Final pass to generate more variations on combined words (e.g., leetspeak on "namepet")
    final_wordlist = set()
    for word in unique_words:
        final_wordlist.add(word)
        final_wordlist.update(generate_case_variations(word))
        final_wordlist.update(generate_leetspeak(word))
        final_wordlist.update(generate_special_char_appending(word))
        final_wordlist.update(generate_number_appending(word, [str(datetime.now().year), str(datetime.now().year)[-2:]])) # Add current year
        # Add common years to appending, e.g., 2020-2025
        for yr in range(datetime.now().year - 5, datetime.now().year + 2):
            final_wordlist.add(f"{word}{yr}")
            final_wordlist.add(f"{word}{str(yr)[-2:]}")

    # Remove duplicates and sort for consistency
    sorted_wordlist = sorted(list(final_wordlist))
    print(f"Generated {len(sorted_wordlist)} unique words.")
    print("-" * 50)
    return sorted_wordlist

def export_wordlist(wordlist, output_file):
    """
    Exports the generated wordlist to a specified text file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in wordlist:
                f.write(word + '\n')
        print(f"Wordlist successfully exported to '{output_file}'")
    except IOError as e:
        print(f"Error exporting wordlist to '{output_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main Program ---
def main():
    parser = argparse.ArgumentParser(
        description="Password Strength Analyzer and Custom Wordlist Generator",
        formatter_class=argparse.RawTextHelpFormatter # For better formatting of help text
    )

    parser.add_argument(
        '-p', '--password',
        type=str,
        help="Analyze the strength of a given password."
    )
    parser.add_argument(
        '-n', '--name',
        type=str,
        help="Name to include in the custom wordlist (e.g., JohnDoe)."
    )
    parser.add_argument(
        '-d', '--date',
        type=str,
        help="Date to include in the custom wordlist (e.g., 1990-05-15, format YYYY-MM-DD)."
    )
    parser.add_argument(
        '-k', '--pet',
        type=str,
        help="Pet's name to include in the custom wordlist (e.g., Buddy)."
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default="custom_wordlist.txt",
        help="Output file name for the generated wordlist (default: custom_wordlist.txt).\n"
             "Only used when generating a wordlist."
    )

    args = parser.parse_args()

    # Password analysis
    if args.password:
        analyze_password_strength(args.password)

    # Wordlist generation
    if args.name or args.date or args.pet:
        generated_words = generate_wordlist(name=args.name, date_str=args.date, pet=args.pet)
        if generated_words:
            export_wordlist(generated_words, args.output)
    elif not args.password: # If no password and no wordlist parameters are given
        print("\nNo operation specified. Use -p for password analysis or provide -n, -d, -k for wordlist generation.")
        parser.print_help()

if __name__ == "__main__":
    main()

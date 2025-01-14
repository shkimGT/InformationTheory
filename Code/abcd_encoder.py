import random

def generate_random_string_and_binary(alphabet, probabilities, num_symbols, encoding_rules):
    """
    Generates a string by sampling from a given probability distribution over an alphabet
    and encodes it into binary strings using all specified encoding rules.

    Parameters:
        alphabet (list): A list of letters representing the alphabet.
        probabilities (list): A list of probabilities corresponding to each letter in the alphabet.
        num_symbols (int): Number of symbols to generate.
        encoding_rules (dict): A dictionary of encoding rules where keys are code versions (1, 2, 3),
                               and values are dictionaries mapping alphabet symbols to binary strings.

    Returns:
        None: Prints the generated string, its binary encodings for each code, and their sizes.
    """
    # Check that the probabilities sum to 1
    if not (abs(sum(probabilities) - 1.0) < 1e-6):
        raise ValueError("Probabilities must sum to 1.")

    # Validate encoding rules
    for code_version, code in encoding_rules.items():
        if not all(symbol in code for symbol in alphabet):
            raise ValueError(f"Code version {code_version} is missing mappings for some symbols in the alphabet.")

    # Generate symbols based on the probability distribution
    generated_symbols = random.choices(alphabet, weights=probabilities, k=num_symbols)

    # Generate the string from symbols
    generated_string = ''.join(generated_symbols)
    print(f"Generated String: {generated_string}")

    # Encode the string using each code and print the results
    for code_version, code in encoding_rules.items():
        binary_string = ''.join(code[symbol] for symbol in generated_symbols)
        print(f"\nCode Version {code_version}:")
        print(f"Encoded Binary String: {binary_string}")
        print(f"Size of Binary String: {len(binary_string)} bits")

# Example usage
alphabet = ['A', 'B', 'C', 'D']
probabilities = [0.5, 0.25, 0.125, 0.125]
num_symbols = 100

encoding_rules = {
    1: {'A': '00', 'B': '01', 'C': '10', 'D': '11'},
    2: {'A': '0', 'B': '1', 'C': '00', 'D': '11'},
    3: {'A': '0', 'B': '10', 'C': '110', 'D': '111'}
}

generate_random_string_and_binary(alphabet, probabilities, num_symbols, encoding_rules)


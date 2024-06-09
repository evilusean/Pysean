import difflib

def compare_code(code1, code2):
    """
    Compares two code snippets and returns a list of line numbers that are different.

    Args:
        code1 (str): The first code snippet. - will be the line that is printed out
        code2 (str): The second code snippet.

    Returns:
        list: A list of line numbers that are different.
    """

    # Split the code snippets into lines.
    lines1 = code1.splitlines()
    lines2 = code2.splitlines()

    # Use the difflib library to compare the lines.
    diff = difflib.ndiff(lines1, lines2)

    # Extract the line numbers of the differences.
    different_lines = []
    for line in diff:
        if line.startswith('-') or line.startswith('+'):
            line_number = int(line[2:])
            different_lines.append(line_number)

    return different_lines

# Example usage:
code1 = """
def add_two_numbers(a, b):
    return a + b
"""

code2 = """
def add_two_numbers(a, b):
    return a + b + 1
"""

# Get the list of different line numbers.
different_lines = compare_code(code1, code2)

# Print the different line numbers.
print("Different lines:", different_lines)

# Print the line of code with the code
for line_number in different_lines:
    print(f"Line {line_number}: {code1.splitlines()[line_number - 1]}")

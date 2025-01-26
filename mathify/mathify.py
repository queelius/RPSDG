#!/usr/bin/env python3
"""
mathify.py

A command-line tool to convert LaTeX math expressions within a string
to Unicode or ASCII representations, preserving the order of operations.

Usage:
    echo "Here is a fraction \(\frac{2^{3y}}{4}\), thanks!" | ./mathify.py
"""

import re
import sys
from pylatexenc.latex2text import LatexNodes2Text, LatexNodes2TextOptions

def convert_latex_to_unicode(text):
    """
    Convert LaTeX math expressions in the input text to Unicode,
    ensuring correct order of operations by adding parentheses.

    Parameters:
        text (str): The input text containing LaTeX expressions.

    Returns:
        str: The text with LaTeX expressions converted to Unicode.
    """
    # Regular expression to find LaTeX math expressions
    # Handles:
    #   - Inline math: \( ... \) or $ ... $
    #   - Display math: \[ ... \] or $$ ... $$
    math_pattern = re.compile(
        r'(\\\[(.*?)\\\])'       # Display math \[ ... \]
        r'|(\$\$(.*?)\$\$)'      # Display math $$ ... $$
        r'|(\\\((.*?)\\\))'      # Inline math \( ... \)
        r'|(\$(.*?)\$)',         # Inline math $ ... $
        re.DOTALL
    )

    # Initialize the converter with LatexNodes2TextOptions
    options = LatexNodes2TextOptions(
        macros={},          # Add any custom macros if needed
        ignore_math=False   # Ensure math expressions are converted
    )
    converter = LatexNodes2Text(options=options)

    def replacer(match):
        """
        Replacement function to convert LaTeX to Unicode, adding parentheses
        around fractions and roots to preserve order of operations.

        Parameters:
            match (re.Match): The regex match object.

        Returns:
            str: The Unicode equivalent of the LaTeX expression.
        """
        # Determine which group matched
        latex_expr = None
        if match.group(2):
            # \[ ... \]
            latex_expr = match.group(2)
        elif match.group(4):
            # $$ ... $$
            latex_expr = match.group(4)
        elif match.group(6):
            # \( ... \)
            latex_expr = match.group(6)
        elif match.group(8):
            # $ ... $
            latex_expr = match.group(8)

        if latex_expr:
            try:
                # Convert LaTeX to Unicode
                unicode_text = converter.latex_to_text(latex_expr)

                # Post-processing to add parentheses around fractions and roots
                # This is a heuristic approach and may need adjustments based on input complexity

                # Add parentheses around fractions to preserve grouping
                unicode_text = re.sub(r'(?<!\\)/', r')/', unicode_text)
                unicode_text = re.sub(r'/', r'/((', unicode_text)

                # Add parentheses around square roots
                unicode_text = re.sub(r'√', r'√(', unicode_text)
                unicode_text += ')'  # Closing parenthesis for the last square root

                # Alternatively, ensure that complex expressions are wrapped in parentheses
                # This method may need refinement based on specific use cases

            except Exception as e:
                # In case of conversion error, return the original LaTeX expression
                unicode_text = f"[Error converting LaTeX: {latex_expr}]"

            return unicode_text
        else:
            # If no LaTeX expression is found, return the original match
            return match.group(0)

    # Replace all LaTeX math expressions with their Unicode equivalents
    return math_pattern.sub(replacer, text)

def main():
    """
    Main function to handle command-line input and output.
    """
    if sys.stdin.isatty():
        # If no input is piped, show usage instructions
        print(__doc__)
        sys.exit(1)

    # Read input from stdin
    input_text = sys.stdin.read()

    # Convert LaTeX to Unicode
    output_text = convert_latex_to_unicode(input_text)

    # Print the result
    print(output_text)

if __name__ == "__main__":
    main()

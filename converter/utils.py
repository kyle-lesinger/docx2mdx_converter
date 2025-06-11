#!/usr/bin/env python3

import os
import re
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString

def get_yaml_instance():
    """
    Returns a configured instance of the YAML parser.

    Returns:
        YAML: Configured YAML instance.
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True  # Ensures YAML formatting is preserved
    yaml.representer.add_representer(PreservedScalarString, literal_presenter)
    return yaml

def color_converter(color, hex_or_rgb="rgb"):
    """
    Converts a hex color code to an RGB tuple, or vice versa.

    Args:
        color (str or tuple): Hex color string in the format "#RRGGBB" or "RRGGBB",
                              or an RGB tuple (R, G, B).
        hex_or_rgb (str): Desired output format. Either "rgb" or "hex".

    Returns:
        str or tuple: Converted color in the requested format.
    """
    
    # Case 1: Input is already an RGB tuple (e.g., (255, 0, 0)).
    if isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        if hex_or_rgb == "rgb":
            return color # Return as is if RGB is requested.
        else:
            return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}" # Convert to HEX.

    # Case 2: Input is an RGB string (e.g., "rgb(255, 0, 0)" or "rgb(255,0,0)").
    # Regex captures three groups of 1-3 digits, allowing for optional spaces around commas.
    rgb_match = re.match(r"rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", str(color))
    if rgb_match:
        rgb_tuple = tuple(map(int, rgb_match.groups())) # Convert captured groups to integers.
        if hex_or_rgb == "rgb":
            return rgb_tuple # Return as tuple if RGB is requested.
        else:
            return f"#{rgb_tuple[0]:02X}{rgb_tuple[1]:02X}{rgb_tuple[2]:02X}" # Convert to HEX.

    # Case 3: Input is a HEX string (e.g., "#FF0000" or "FF0000").
    hex_color_str = str(color).lstrip("#").upper()  # Remove '#' and convert to uppercase for consistent processing.
    if len(hex_color_str) == 6 and all(c in "0123456789ABCDEF" for c in hex_color_str): # Validate hex format.
        if hex_or_rgb == "hex":
            return f"#{hex_color_str}" # Return normalized HEX if HEX is requested.
        else:
            # Convert HEX to RGB tuple.
            rgb_tuple = tuple(int(hex_color_str[i:i+2], 16) for i in (0, 2, 4))
            return rgb_tuple

    # If none of the above cases match, the format is invalid.
    raise ValueError("Invalid color format. Must be RGB (rgb(R,G,B) or (R,G,B)) or HEX (#RRGGBB or RRGGBB)")


def literal_presenter(dumper, data):
    """
    Ensures YAML scalar strings are represented correctly as block literals.

    Args:
        dumper: YAML dumper instance.
        data (str): The data to be presented as a block literal.

    Returns:
        YAML scalar string.
    """
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

def convert_docx_to_mdx_path(docx_path):
    """
    Converts a .docx file path to a .data.mdx file path within the 'markdown' directory.

    Args:
        docx_path (str): The original .docx file path.

    Returns:
        str: The modified path with .data.mdx extension in 'markdown' directory.
    """
    out_dir = "markdown"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.basename(docx_path)  # Extract filename
    new_filename = re.sub(r"\.docx$", ".data.mdx", filename)  # Replace .docx with .data.mdx
    return os.path.join(out_dir, new_filename)

def save_mdx_content(outfile, mdx_content_string):
    """
    Saves the fully formed MDX content string to a file.

    Args:
        outfile (str): Output file path.
        mdx_content_string (str): The complete MDX content.

    Returns:
        int: 0 on success.
    """
    with open(outfile, "w", encoding="utf-8") as file:
        print(f"Writing file: {outfile}")
        file.write(mdx_content_string)
    return 0


def debug_mdx_file(mdx_file_path):
    """
    Reads the file and prints its content to debug the presence of '|2-' or other anomalies.
    """
    with open(mdx_file_path, "r", encoding="utf-8") as file:
        content = file.readlines()  # Read all lines

    print("\n[DEBUG] FULL FILE CONTENT (showing raw formatting):")
    for i, line in enumerate(content, start=1):
        print(f"{i}: {repr(line)}")  # Show raw representation including spaces and escape sequences

    print("\n[DEBUG] Searching for '|2-' occurrences:")
    problematic_lines = [line for line in content if "|2-" in line]

    if problematic_lines:
        for line in problematic_lines:
            print(f"Found: {repr(line)}")
    else:
        print("No '|2-' found. The issue might be elsewhere.")


def remove_trailing_whitespace(file_path):
    """Removes trailing whitespace from each line in the specified file."""
    print('Removing whitespaces after each line')
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip trailing whitespace from each line and ensure a newline character at the end.
    cleaned_lines = [line.rstrip() + "\n" for line in lines]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print(f"\n✅ {file_path} complete.")

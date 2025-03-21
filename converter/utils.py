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
    
    # ✅ If input is already an RGB tuple, check if conversion is needed
    if isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        return color if hex_or_rgb == "rgb" else f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

    # ✅ If input is an RGB string (e.g., "rgb(255, 0, 0)"), convert it to tuple
    rgb_match = re.match(r"rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", str(color))
    if rgb_match:
        rgb_tuple = tuple(map(int, rgb_match.groups()))
        return rgb_tuple if hex_or_rgb == "rgb" else f"#{rgb_tuple[0]:02X}{rgb_tuple[1]:02X}{rgb_tuple[2]:02X}"

    # ✅ If input is HEX, process it
    hex_color = str(color).lstrip("#").upper()  # Normalize case
    if len(hex_color) == 6 and all(c in "0123456789ABCDEF" for c in hex_color):
        # Convert HEX to RGB
        rgb_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return rgb_tuple if hex_or_rgb == "rgb" else f"#{hex_color}"  # Keep HEX if no conversion needed

    raise ValueError("Invalid color format. Must be RGB (rgb(R,G,B)) or HEX (#RRGGBB)")


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

def clean_mdx_file(mdx_file_path):
    """
    Cleans up erroneous text in an MDX file, replacing known issues.

    Args:
        mdx_file_path (str): Path to the MDX file to clean.

    Returns:
        str: Confirmation message.
    """
    with open(mdx_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Debug: Print lines containing "|2-" before replacement
    problematic_lines = [line for line in content.split("\n") if "|2-" in line]
    if problematic_lines:
        print("\n[DEBUG] Found occurrences of '|2-' before replacement:")
        for line in problematic_lines:
            print(line)

    # Ensure ALL "|X-" variations are replaced with "|"
    content = re.sub(r"\|\d+-", "|", content)
    content = re.sub(r"\|[^\S\r\n]*[^\s]*-", "|", content) #remove |- with only |


    # Debug: Check if "|2-" still exists after replacement
    if "|2-" in content:
        print("[ERROR] '|2-' was NOT fully removed!")

    with open(mdx_file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return print(f"\n✅  File {mdx_file_path} processed and cleaned successfully.")

def save_mdx_file(outfile, output_data):
    """
    Saves YAML-structured data to an MDX file.

    Args:
        outfile (str): Output file path.
        output_data (dict): Dictionary containing the YAML data.

    Returns:
        int: 0 on success.
    """
    yaml = get_yaml_instance()
    with open(outfile, "w", encoding="utf-8") as file:
        print(f"Writing file: {outfile}")
        file.write("---\n")
        yaml.dump(output_data, file)
        file.write("\n---\n\n")
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
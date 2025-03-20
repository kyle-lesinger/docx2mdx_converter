#!/usr/bin/env python3
from ruamel.yaml.scalarstring import PreservedScalarString
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString
import utils

def generate_mdx_content_headers(table_1):
    """
    Generate structured MDX content with blocks and prose.

    Args:
        table_1 (dict): Dictionary containing metadata (e.g., temporal extent, resolution).
        content_text (str): The main content block with headers.

    Returns:
        str: Formatted MDX content as a string.
    """
    
    return PreservedScalarString(f"""\
<Block>
  <Prose>   
    **Temporal Extent:** {table_1.get('start_temporal_extent', 'N/A')} - {table_1.get('end_temporal_extent', 'N/A')}<br />
    **Temporal Resolution:** {table_1.get('temporal_resolution', ['N/A'])[0]}<br />
    **Spatial Extent:** {table_1.get('spatial_extent', ['N/A'])[0]}<br />
    **Spatial Resolution:** {table_1.get('spatial_resolution', ['N/A'])[0]}<br />
    **Data Type:** {table_1.get('data_type', ['N/A'])[0]}<br />
    **Data Latency:** {table_1.get('data_latency', ['N/A'])[0]}<br />
  </Prose>
</Block>\n\n""")


def add_prose_to_final_mdx(outfile, prose_blocks):
    """
    Save the final MDX file with the correct structure.

    Args:
        outfile (str): The output MDX file path.
        yaml_content (dict): The YAML front matter content.
        prose_blocks (str): Additional prose content to append after the YAML block.

    Returns:
        int: 0 on success.
    """
    yaml = utils.get_yaml_instance()  # Ensure correct YAML formatting
    
    with open(outfile, "r", encoding="utf-8") as file:
        existing_content = file.read().strip()  # Strip extra spaces at the end

    # print(f"Adding additional prose to {outfile}")
    formatted_blocks = "\n\n" + prose_blocks.strip() + "\n\n"

    # Append to file
    with open(outfile, "w", encoding="utf-8") as file:
        file.write(existing_content + formatted_blocks)

    return


def format_prose_block(content, header=None):
    """
    Formats prose content into a properly indented Block/Prose structure.

    Args:
        content (str): Text content for the prose block.
        header (str, optional): Optional header for the prose section.

    Returns:
        str: Formatted MDX prose block with consistent indentation.
    """

    formatted_paragraphs = "\n\n".join(
        f"    {line.strip()}" for line in content[header].split("\n") if line.strip()
    )  # Ensure all paragraphs have uniform indentation

    if header != 'Introduction paragraph':
        return PreservedScalarString(f"""\
<Block>
  <Prose>
    ## {header}
{formatted_paragraphs}
  </Prose>
</Block>\n\n""")
    
    return PreservedScalarString(f"""\
<Block>
  <Prose>
{formatted_paragraphs}
  </Prose>
</Block>\n\n""")

    
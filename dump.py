#!/usr/bin/env python3
from converter import parse as par
from converter import utils
from converter import prose
import sys
import os
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString
import re

#Testing data
# docx_path = "template/test_LIS.docx" # Example filename for testing
# hex_or_rgb = 'rgb'


#Set order of prose_blocks
orderTOP = ['Introduction paragraph', 'Source Data Product Citation', 'Version History', 'Scientific Details']
#Between orderTOP and orderBOTTOM, any optional prose blocks will be added automatically
orderBOTTOM = ['Disclaimer','Limitations of Use','License']



if __name__ == '__main__':
    docx_path=sys.argv[1]  # Name of input file
    hex_or_rgb = sys.argv[2]
    
    #First accumulate the information from the docx file into different objects
    table_0, table_1, table_optional, prose_content = par.retrieve_all_docx_data(docx_path)
    #Build non prose section according to .mdx shcema
    output = prose.construct_non_prose_section(table_0, table_1, prose_content, hex_or_rgb)

    outfile = utils.convert_docx_to_mdx_path(docx_path)

    # --- Assemble MDX content ---
    mdx_parts = []

    # 1. Add YAML frontmatter
    yaml_instance = utils.get_yaml_instance()
    import io
    string_stream = io.StringIO()
    yaml_instance.dump(output, string_stream)
    frontmatter_yaml = f"---\n{string_stream.getvalue()}---\n\n"
    mdx_parts.append(frontmatter_yaml)

    # 2. Add MDX content headers (e.g., dataset summary block)
    mdx_parts.append(prose.generate_mdx_content_headers(table_1))

    # 3. Add REQUIRED TOP prose blocks (Introduction, Citation, etc.)
    for header in orderTOP:
        if header in prose_content: # Check if the prose section exists in the parsed data
            mdx_parts.append(prose.format_prose_block(prose_content, header))

    # 4. Add OPTIONAL prose blocks found in table_optional
    if len(table_optional) > 0:
        for k,v in table_optional.items():
            # Assuming table_optional stores a list of dictionaries,
            # and each dictionary has the prose content under its key.
            # Example: table_optional = {"Optional Section": [{"Optional Section": "Content..."}]}
            # The key_ extraction might need adjustment based on actual structure.
            if isinstance(table_optional[k], list) and len(table_optional[k]) > 0 and isinstance(table_optional[k][0], dict):
                key_ = list(table_optional[k][0].keys())[0] # Get the actual header name
                mdx_parts.append(prose.format_prose_block(table_optional[k][0], key_))

    # 5. Add REQUIRED BOTTOM prose blocks (Disclaimer, License, etc.)
    for header in orderBOTTOM:
        if header in prose_content: # Check if the prose section exists
            mdx_parts.append(prose.format_prose_block(prose_content, header))

    # --- Save the final MDX file ---
    final_mdx_content = "".join(mdx_parts) # Combine all parts into a single string
    utils.save_mdx_content(outfile, final_mdx_content) # Save the complete MDX content

    # --- Post-processing and debugging ---
    utils.debug_mdx_file(outfile) # Output file content for debugging
    utils.remove_trailing_whitespace(outfile)

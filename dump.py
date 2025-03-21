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
orderBOTTOM = ['Limitations of Use','License']



if __name__ == '__main__':
    docx_path=sys.argv[1]  # Name of input file
    hex_or_rgb = sys.argv[2]
    
    #First accumulate the information from the docx file into different objects
    table_0, table_1, table_optional, prose_content = par.retrieve_all_docx_data(docx_path)
    #Build non prose section according to .mdx shcema
    output = prose.construct_non_prose_section(table_0, table_1, table_optional, prose_content, hex_or_rgb)

    #Save file because appending wasn't working very well
    outfile = utils.convert_docx_to_mdx_path(docx_path)
    utils.save_mdx_file(outfile, output)

    #Append to the saved .data.mdx file for each of the prose section
    prose.add_prose_to_final_mdx(outfile,prose.generate_mdx_content_headers(table_1))

    #REQUIRED HEADER AND CONTENT INFORMATION
    for idx, header in enumerate(orderTOP):
        try:
            prose.add_prose_to_final_mdx(outfile,prose.format_prose_block(prose_content,header))
        except KeyError:
            pass

    #OPTIONAL HEADER AND CONTENT INFORMATION
    if len(table_optional) > 0:
        for k,v in table_optional.items():
            key_ = list(table_optional[k][0].keys())[0]
            prose.add_prose_to_final_mdx(outfile,prose.format_prose_block(table_optional[k][0],key_))

    #REQUIRED ENDING INFORMATION
    for idx, header in enumerate(orderBOTTOM):
        prose.add_prose_to_final_mdx(outfile,prose.format_prose_block(prose_content,header))

    # utils.debug_mdx_file(outfile)
    utils.clean_mdx_file(outfile)

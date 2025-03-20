#!/usr/bin/env python3

import parse as par
import utils
import prose
import sys
import os
import yaml
import json
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString
import re

#Testing data
# docx_path = "test_LIS.docx" # Example filename for testing
# hex_or_rgb = 'rgb'


def construct_non_prose_section(table_0, table_1, table_2, content):
    """
    Constructs a non-prose section of the document.
    """
    # Construct output dictionary
    output = {
        "id": table_0["id"],
        "name": table_0["name"],
        "description": json.loads(f'"{table_0["description"]}"'),
        "media": {
            "src": f"::file {table_0['media'][0]['main_media_image']}",
            "alt": table_0['media'][1]['main_fig_alt_text'],
            "author": {
                "name": table_0['media'][2]['main_fig_author_name'],
                "url": table_0['media'][3]['main_fig_author_URL']
            }
        },
        "taxonomy": [
            {"name": "Topics", "values": table_0["tags"][0]["topic"].split(", ")},
            {"name": "Source", "values": [table_0["tags"][1]["source"]]}
        ],
        "infoDescription": PreservedScalarString(f"""\
    ::markdown 
        - Temporal Extent: {table_1.get('start_temporal_extent', 'N/A')} - {table_1.get('end_temporal_extent', 'N/A')}
        - Temporal Resolution: {table_1.get('temporal_resolution', ['N/A'])[0]}
        - Spatial Extent: {table_1.get('spatial_extent', ['N/A'])[0]}
        - Spatial Resolution: {table_1.get('spatial_resolution', ['N/A'])[0]}
        - Data Units: {table_1.get('data_units', ['N/A'])[0]}
        - Data Type: {table_1.get('data_type', ['N/A'])[0]}
        - Data Latency: {table_1.get('data_latency', ['N/A'])[0]}
    """)
    }

    output["layers"] = []

    max_layers = 20 #This is just a filler. Once a number is not reached it will stop

    for i in range(max_layers):
        try:
            layer_data = table_0["layers"][i][f"Layer{i}"]  # Extract specific layer dictionary
            subset = table_0["layers"][i][f'Layer{i}']
            output["layers"].append({
                "id": subset.get(f"layer_id{i}"),
                "stacCol": subset.get(f"stacCol{i}"),
                "stacApiEndpoint": "https://dev.openveda.cloud/api/stac",
                "name": subset.get(f"layer_name{i}"),
                "type": "raster",
                "description": subset.get(f"layer_description{i}"),
                "initialDatetime": "newest",
                "projection": {"id": "equirectangular"},
                "zoomExtent": [0, 20],
                "legend": {
                    "unit": {"label": subset.get(f"units{i}")},
                    "type": "gradient",
                    "min": 0,
                    "max": 100,
                    "stops": [f"rgb({','.join(map(str, utils.color_converter(stop)))})" if hex_or_rgb=='rgb' else stop for stop in subset.get(f'color_stops{i}', [])]
                } if subset.get(f'color_stops{i}') else {},  # Handle empty color_stops case
                "info": {
                    "source": table_1['content_source'][0],
                    "spatialExtent": table_1['spatial_extent'][0],
                    "temporalResolution": table_1['temporal_resolution'][0],
                    "unit": table_1['data_units'][0]
                },
                "media": {
                    "src": "::file <INSERT MANUALLY>",
                    "alt": "<INSERT MANUALLY>"
                }
            }
            )
        except IndexError:
            pass
    return output


#Set order of prose_blocks
orderTOP = ['Introduction paragraph', 'Source Data Product Citation', 'Version History', 'Scientific Details']
orderBOTTOM = ['Limitations of Use','License']


if __name__ == '__main__':
    docx_path=sys.argv[1]  # Name of input file
    hex_or_rgb = sys.argv[2]
    # Initialize ruamel.yaml to enforce proper formatting
    outfile = utils.convert_docx_to_mdx_path(docx_path)
    table_0, table_1, table_optional, prose_content = par.retrieve_all_docx_data(docx_path)
    output = construct_non_prose_section(table_0, table_1, table_optional, prose_content)
    utils.save_mdx_file(outfile, output)
    prose.add_prose_to_final_mdx(outfile,prose.generate_mdx_content_headers(table_1))

    #REQUIRED HEADER AND CONTENT INFORMATION
    for idx, header in enumerate(orderTOP):
        prose.add_prose_to_final_mdx(outfile,prose.format_prose_block(prose_content,header))

    #OPTIONAL HEADER AND CONTENT INFORMATION
    if len(table_optional) > 0:
        for k,v in table_optional.items():
            key_ = list(table_optional[k][0].keys())[0]
            prose.add_prose_to_final_mdx(outfile,prose.format_prose_block(table_optional[k][0],key_))

    #REQUIRED ENDING INFORMATION
    for idx, header in enumerate(orderBOTTOM):
        prose.add_prose_to_final_mdx(outfile,prose.format_prose_block(prose_content,header))

    # output['structuredContent'] = generate_mdx_content_headers(table_1)

    
    # utils.clean_mdx_file(outfile)

#!/usr/bin/env python3
from ruamel.yaml.scalarstring import PreservedScalarString
from ruamel.yaml import YAML
from converter import utils
from converter import verify
import json

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


def construct_non_prose_section(table_0, table_1, table_2, content, hex_or_rgb):
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

            # print(subset.get(f"rescale_max{i}"))

            output["layers"].append({
                "id": subset.get(f"layer_id{i}"),
                "stacCol": subset.get(f"stacCol{i}"),
                "stacApiEndpoint": "https://dev.openveda.cloud/api/stac",
                "name": subset.get(f"layer_name{i}"),
                "type": subset.get(f"data_format{i}"),
                "description": subset.get(f"layer_description{i}"),
                "initialDatetime": "newest",
                "projection": {"id": verify.check_if_projection_is_valid(subset.get(f"projection{i}"))},
                "zoomExtent": [0, 20],
                "sourceParams": {
                    "colormap_name": verify.check_if_colormap_is_valid(subset.get(f"colormap_name{i}")),
                    "rescale": [float(subset.get(f"rescale_min{i}")),float(subset.get(f"rescale_max{i}"))],
                    "resampling": subset.get(f"resampling{i}")                                           
                },
                "compare": {
                    "datasetId": subset.get(f"layer_id{i}"), #We are setting the id as the file ID just for simplicity
                    "layerId": subset.get(f"layer_id{i}"),
                "mapLabel": PreservedScalarString("""\
::js ({ dateFns, datetime, compareDatetime }) => {
return `${dateFns.format(datetime, 'LLL yyyy')} VS ${dateFns.format(compareDatetime, 'LLL yyyy')}`;
}""")
                },
                "legend": {
                    "unit": {"label": subset.get(f"units{i}")},
                    "type": subset.get(f"legend_type{i}"),
                    "min": float(subset.get(f"legend_minimum{i}")) if subset.get(f"legend_type{i}") == 'gradient' else '',
                    "max": float(subset.get(f"legend_maximum{i}")) if subset.get(f"legend_type{i}") == 'gradient' else '',
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


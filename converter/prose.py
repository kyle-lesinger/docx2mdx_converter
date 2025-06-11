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
    
    return f"""\
<Block>
  <Prose>   
    **Temporal Extent:** {table_1.get('start_temporal_extent', 'N/A')} - {table_1.get('end_temporal_extent', 'N/A')}<br />
    **Temporal Resolution:** {table_1.get('temporal_resolution', ['N/A'])[0]}<br />
    **Spatial Extent:** {table_1.get('spatial_extent', ['N/A'])[0]}<br />
    **Spatial Resolution:** {table_1.get('spatial_resolution', ['N/A'])[0]}<br />
    **Data Type:** {table_1.get('data_type', ['N/A'])[0]}<br />
    **Data Latency:** {table_1.get('data_latency', ['N/A'])[0]}<br />
  </Prose>
</Block>\n\n"""


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
        return f"""\
<Block>
  <Prose>
    ## {header}
{formatted_paragraphs}
  </Prose>
</Block>\n\n"""
    
    return f"""\
<Block>
  <Prose>
{formatted_paragraphs}
  </Prose>
</Block>\n\n"""


def _build_media_block(media_data_list):
    """
    Constructs the 'media' block for the YAML frontmatter.

    Args:
        media_data_list (list): A list of dictionaries, where each dictionary
                                represents a piece of media metadata (e.g., image source,
                                alt text, author information). Expected to come from
                                table_0.get("media", []).

    Returns:
        dict: A dictionary representing the structured media block.
    """
    src_val = None  # Default to None if no main_media_image is found
    alt_text = "Data not provided"
    author_name = "Data not provided"
    author_url = "Data not provided"

    if isinstance(media_data_list, list):
        for item in media_data_list:
            # Check for main image source
            if item.get('main_media_image'):
                src_val = f"::file {item['main_media_image']}" # Format as MDX file link
            # Check for alt text
            if item.get('main_fig_alt_text'):
                alt_text = item['main_fig_alt_text']
            # Check for author name
            if item.get('main_fig_author_name'):
                author_name = item['main_fig_author_name']
            # Check for author URL
            if item.get('main_fig_author_URL'):
                author_url = item['main_fig_author_URL']

    return {
        "src": src_val,  # This can be None if no image is specified
        "alt": alt_text, # Default "Data not provided"
        "author": {
            "name": author_name, # Default "Data not provided"
            "url": author_url    # Default "Data not provided"
        }
    }

def _build_taxonomy_block(tags_data_list):
    """
    Constructs the 'taxonomy' block for the YAML frontmatter.

    Args:
        tags_data_list (list): A list of dictionaries, where each dictionary
                               contains tag information (e.g., topic, subtopic, source).
                               Expected to come from table_0.get("tags", []).

    Returns:
        list: A list of dictionaries, each representing a taxonomy category.
    """
    topics = []
    subtopics = []
    source = "Data not provided" # Default source

    if isinstance(tags_data_list, list):
        for item in tags_data_list:
            # Extract and clean topics (comma-separated string to list of strings)
            if item.get('topic'):
                topics = [t.strip() for t in item['topic'].split(",") if t.strip()]
            # Extract and clean subtopics
            if item.get('subtopic'):
                subtopics = [st.strip() for st in item['subtopic'].split(",") if st.strip()]
            # Extract source
            if item.get('source'):
                source = item['source']

    return [
        {"name": "Topics", "values": topics if topics else ["Data not provided"]}, # Default if no topics
        {"name": "Subtopics", "values": subtopics if subtopics else ["Data not provided"]}, # Default if no subtopics
        {"name": "Source", "values": [source]} # Source will have its default if not found
    ]

def construct_non_prose_section(table_0, table_1, content, hex_or_rgb):
    """
    Constructs the main non-prose (YAML frontmatter) section of the MDX document.

    Args:
        table_0 (dict): Dictionary containing general metadata, media, tags, and layers info.
        table_1 (dict): Dictionary containing specific dataset attributes.
        content (dict): Dictionary containing prose content extracted from paragraphs. (Unused in this function)
        hex_or_rgb (str): String indicating color format ('hex' or 'rgb').

    Returns:
        dict: A dictionary representing the complete YAML frontmatter.
    """
    # Assemble the main output dictionary for YAML frontmatter
    output = {
        "id": table_0.get("id"),  # Unique identifier for the dataset
        "name": table_0.get("name"), # Name of the dataset
        # Description, processed via json.loads to handle potential special characters
        "description": json.loads(f'"{table_0.get("description","")}"'),
        "media": _build_media_block(table_0.get("media", [])), # Structured media information
        "taxonomy": _build_taxonomy_block(table_0.get("tags", [])), # Structured taxonomy information
        # Markdown formatted string for various informational details
        "infoDescription": PreservedScalarString(f"""\
    ::markdown 
        - Temporal Extent: {table_1.get('start_temporal_extent', 'N/A')} - {table_1.get('end_temporal_extent', 'N/A')}
        - Temporal Resolution: {table_1.get('temporal_resolution', ['N/A'])[0]}
        - Spatial Extent: {table_1.get('spatial_extent', ['N/A'])[0]}
        - Spatial Resolution: {table_1.get('spatial_resolution', ['N/A'])[0]}
        - Data Units: {table_1.get('data_units', ['N/A'])[0]}
        - Data Type: {table_1.get('data_type', ['N/A'])[0]}
        - Data Latency: {table_1.get('data_latency', ['N/A'])[0]}
    """.strip()) # .strip() to prevent YAML artifacts from leading/trailing whitespace
    }

    output["layers"] = [] # Initialize empty list for layer data

    # JavaScript code for the map label in compare mode, kept as a PreservedScalarString
    MAP_LABEL_JS_CODE = (
        "::js ({ dateFns, datetime, compareDatetime }) => {\n"
        "return `${dateFns.format(datetime, 'LLL yyyy')} VS ${dateFns.format(compareDatetime, 'LLL yyyy')}`;\n"
        "}"
    )

    parsed_layers = table_0.get("layers", []) # Get layer data from table_0, default to empty list

    # Iterate through each layer parsed from the input document
    for i, layer_container_dict in enumerate(parsed_layers):
        actual_layer_data = layer_container_dict.get(f"Layer{i}")
        if not actual_layer_data: # Skip if no data for this layer index
            continue

        # --- Helper function to safely convert string values to float ---
        def safe_float(value_str):
            """
            Safely converts a string value to a float, handling various non-numeric
            placeholders like "Data not provided", "None", etc.
            Returns None if conversion is not possible or input is a placeholder.
            """
            if isinstance(value_str, (int, float)): # Already a number
                return float(value_str)
            if isinstance(value_str, str):
                value_str_cleaned = value_str.strip().lower()
                # Check for common placeholder strings
                if value_str_cleaned and value_str_cleaned not in ["data not provided", "none", "null", ""]:
                    try:
                        return float(value_str.strip()) # Use original case for float conversion
                    except ValueError:
                        return None # Conversion failed
            return None # Not a string or is a placeholder

        # --- Extract and process layer parameters ---
        rescale_min_val = safe_float(actual_layer_data.get(f"rescale_min{i}"))
        rescale_max_val = safe_float(actual_layer_data.get(f"rescale_max{i}"))

        # Build sourceParams dictionary conditionally
        source_params = {}
        colormap_val = actual_layer_data.get(f"colormap_name{i}")
        if colormap_val and str(colormap_val).strip().lower() not in ["data not provided", "none", "null", ""]:
            source_params["colormap_name"] = verify.check_if_colormap_is_valid(str(colormap_val).strip())

        resampling_val = actual_layer_data.get(f"resampling{i}")
        if resampling_val and str(resampling_val).strip().lower() not in ["data not provided", "none", "null", ""]:
            source_params["resampling"] = str(resampling_val).strip()

        if rescale_min_val is not None and rescale_max_val is not None:
            source_params["rescale"] = [rescale_min_val, rescale_max_val]

        # Build legend_dict conditionally
        legend_dict = {}
        legend_units = actual_layer_data.get(f"units{i}")
        legend_type = actual_layer_data.get(f"legend_type{i}")
        legend_min_val = safe_float(actual_layer_data.get(f"legend_minimum{i}"))
        legend_max_val = safe_float(actual_layer_data.get(f"legend_maximum{i}"))
        color_stops_data = actual_layer_data.get(f'color_stops{i}', [])

        if legend_units and str(legend_units).strip().lower() not in ["data not provided", "none", "null", ""]:
            legend_dict["unit"] = {"label": str(legend_units).strip()}

        if legend_type and str(legend_type).strip().lower() not in ["data not provided", "none", "null", ""]:
            legend_type_str = str(legend_type).strip()
            legend_dict["type"] = legend_type_str
            if legend_type_str == 'gradient': # Min/max only relevant for gradient legends
                if legend_min_val is not None:
                    legend_dict["min"] = legend_min_val
                if legend_max_val is not None:
                    legend_dict["max"] = legend_max_val

        if isinstance(color_stops_data, list) and color_stops_data:
            processed_stops = []
            for stop_color in color_stops_data:
                if not stop_color or str(stop_color).strip().lower() in ["data not provided", "none", "null", ""]:
                    continue # Skip invalid or placeholder color stops
                try:
                    # Convert color to the specified format (rgb or hex)
                    if hex_or_rgb == 'rgb':
                        rgb_tuple = utils.color_converter(str(stop_color), 'rgb')
                        processed_stops.append(f"rgb({','.join(map(str, rgb_tuple))})")
                    else:
                        processed_stops.append(utils.color_converter(str(stop_color), 'hex'))
                except ValueError:
                    print(f"Warning: Could not convert color stop '{stop_color}' for layer {i}. Skipping.")
            if processed_stops:
                legend_dict["stops"] = processed_stops

        # Build projection_dict conditionally
        projection_id_val = actual_layer_data.get(f"projection{i}")
        projection_dict = {}
        if projection_id_val and str(projection_id_val).strip().lower() not in ["data not provided", "none", "null", ""]:
            projection_dict["id"] = verify.check_if_projection_is_valid(str(projection_id_val).strip())

        # --- Helper function to get cleaned string values or None ---
        def get_str_val_or_none(key_name):
            """
            Retrieves a string value for a given key from actual_layer_data,
            strips it, and returns None if it's a placeholder or empty.
            Appends the layer index 'i' to the key_name.
            """
            val = actual_layer_data.get(f"{key_name}{i}")
            if val and str(val).strip().lower() not in ["data not provided", "none", "null", ""]:
                return str(val).strip()
            return None

        # Extract basic layer string properties using the helper
        layer_id = get_str_val_or_none("layer_id")
        stac_col = get_str_val_or_none("stacCol")
        layer_name = get_str_val_or_none("layer_name")
        data_format_val = get_str_val_or_none("data_format")
        layer_description = get_str_val_or_none("layer_description")

        main_dataset_id = str(table_0.get("id","")).strip()
        compare_layer_id = layer_id if layer_id else main_dataset_id # Fallback for compare layerId

        # Assemble the layer dictionary
        layer_to_append = {
            "id": layer_id,
            "stacCol": stac_col,
            "stacApiEndpoint": "https://dev.openveda.cloud/api/stac", # Fixed endpoint
            "name": layer_name,
            "type": data_format_val,
            "description": layer_description,
            "initialDatetime": "newest", # Default value
            "zoomExtent": [0, 20], # Default value
            "compare": {
                "datasetId": main_dataset_id,
                "layerId": compare_layer_id,
                "mapLabel": PreservedScalarString(MAP_LABEL_JS_CODE) # Use predefined JS code
            },
            "info": { # Extract info from table_1, providing defaults
                "source": str(table_1.get('content_source', ["Data not provided"])[0]).strip(),
                "spatialExtent": str(table_1.get('spatial_extent', ["Data not provided"])[0]).strip(),
                "temporalResolution": str(table_1.get('temporal_resolution', ["Data not provided"])[0]).strip(),
                "unit": str(table_1.get('data_units', ["Data not provided"])[0]).strip()
            },
            "media": { # Placeholder media block for layers
                "src": "::file <INSERT MANUALLY>",
                "alt": "<INSERT MANUALLY>"
            }
        }

        # Conditionally add non-empty dictionaries
        if source_params: layer_to_append["sourceParams"] = source_params
        if legend_dict: layer_to_append["legend"] = legend_dict
        if projection_dict: layer_to_append["projection"] = projection_dict

        # Clean the assembled layer: remove keys with None, empty string, or empty dict values.
        layer_to_append_cleaned = {k: v for k, v in layer_to_append.items() if v is not None and v != "" and v != {}}
        # Further ensure that if optional blocks like sourceParams are empty they are removed
        if "sourceParams" in layer_to_append_cleaned and not layer_to_append_cleaned["sourceParams"]:
             del layer_to_append_cleaned["sourceParams"]
        if "legend" in layer_to_append_cleaned and not layer_to_append_cleaned["legend"]:
             del layer_to_append_cleaned["legend"]
        if "projection" in layer_to_append_cleaned and not layer_to_append_cleaned["projection"]:
             del layer_to_append_cleaned["projection"]

        # Only append the layer if it has an 'id' after cleaning.
        if layer_to_append_cleaned.get("id"):
            output["layers"].append(layer_to_append_cleaned)
    return output


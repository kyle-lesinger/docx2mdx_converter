# **DOCX to MDX Converter**

## **📌 Overview**
This Python script converts structured **DOCX files** into **MDX (Markdown + JSX)** format, preserving **metadata, content structure, and color formatting** while ensuring **correct spacing, indentation, and color conversions**.

This is specific for NASA VEDA information. Use file template/test_LIS.docx as the template and then fill template/test_LIS.docx in the appropriate information for each section.

## **📌 Restrictions**
This currently should only be run with a **single landing page collection**. For example, Land Information System - Alaska will have four different layers, but will be featured on [VEDA data catalog](https://www.earthdata.nasa.gov/dashboard/data-catalog) as a single item. This script will support an infinite number of layers (as long as the same formatting between layers is used). This set of scripts is still a work in progress depending on your use case and future adjustments will be made.

### **Features:**
- ✅ **Extracts** metadata, structured tables, and formatted text from DOCX (use file test_LIS.docx for the proper format)
- ✅ **Handles multi-layered data** (e.g., having more than one input layer)
- ✅ **Converts colors** between **Hex ↔ RGB** if needed
- ✅ **Appends structured prose sections** dynamically

---

## **📦 Installation**
### **🔹 Prerequisites**
Ensure you have **Python 3.7+** installed.

### **🔹 Required Dependencies**
Run:
```bash
pip install -r requirements.txt
```
OR install manually:
```bash
pip install ruamel.yaml
```

---

## **📝 Usage**
### **🔹 Converting a DOCX file to MDX**
Run the script with:
```bash
python dump.py /path/to/input.docx rgb_or_hex_string
```
Example:
```bash
python dump.py "template/test_LIS.docx" "rgb"
```
or
```bash
python dump.py "template/test_LIS.docx" "hex"
```

This **automatically:**
- Parses the DOCX file
- Extracts metadata
- Converts it into a **structured MDX file**
- Saves it in the `converted_markdown/` directory

---

## **🛠️ Functionality Breakdown**
### **🔹 1. YAML Processing**
- **Extracts DOCX table contents**
- Formats them into **YAML front matter**
- Removes any YAML errors (e.g., `|2-`)

🔹 **Function:** `get_yaml_instance()`

```python
def get_yaml_instance():
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    yaml.representer.add_representer(PreservedScalarString, literal_presenter)
    return yaml
```

---

### **🔹 2. Color Conversion (Hex ↔ RGB)**
Automatically converts **colors between Hex and RGB** based on user preference.

🔹 **Function:** `color_converter()`
```python
def color_converter(color, hex_or_rgb="rgb"):
    """
    Converts Hex ↔ RGB based on user preference.
    """
```
✅ Converts `#FF5733` → `(255, 87, 51)`  
✅ Converts `rgb(255, 87, 51)` → `#FF5733`  
✅ **Keeps format intact** if already correct  

---

### **🔹 3. Converting DOCX file to MDX**
Extracts **table data, metadata, and prose blocks** while preserving formatting.

🔹 **Function:** `convert_docx_to_mdx_path()`
```python
def convert_docx_to_mdx_path(docx_path):
    """
    Converts a .docx file path to .data.mdx in 'converted_markdown'.
    """
```
- Creates `converted_markdown/` folder
- **Renames `.docx` → `.data.mdx`**
- Saves the formatted MDX file

---

### **🔹 4. Cleaning MDX Formatting**
Fixes YAML errors by removing artifacts like `|2-`

🔹 **Function:** `clean_mdx_file()`
```python
def clean_mdx_file(mdx_file_path):
    """
    Removes unwanted artifacts from MDX file.
    """
```
✅ **Fixes spacing issues**  
✅ **Ensures MDX renders correctly**

---

### **🔹 5. Adding Prose Blocks**
Dynamically appends prose sections without **overwriting existing content**.

🔹 **Function:** `add_prose_to_final_mdx()`
```python
def add_prose_to_final_mdx(outfile, prose_blocks):
    """
    Appends prose blocks while preserving spacing.
    """
```
✅ **Adds new `<Block>` sections**  
✅ **Maintains proper indentation**  
✅ **Prevents formatting corruption**

---

## **📂 Output Example**
Your **final MDX file** will look like this:

```mdx
---
id: lis-alaska-nrt
name: Land Information System - Alaska
description: State of Alaska vegetation and hydrological information produced by NASA’s
  Short-term Prediction and Transition Center – Land Information System (SPoRT-LIS).

layers:
  - id: alaska_relative_soil_moisture_10cm
    stacCol: lis_ak_rsm_10cm
    stacApiEndpoint: https://dev.openveda.cloud/api/stac
    name: Relative Soil Moisture (0-10cm), Updated Daily
    type: raster
    description: Relative soil moisture (RSM) is a ratio of the volumetric soil moisture
      between the wilting and saturation points for a given soil type.
    legend:
      unit:
        label: Percentage %
      type: gradient
      min: 0
      max: 100
      stops:
        - rgb(60,40,180)
        - rgb(111,96,219)
        - rgb(160,139,255)
        - rgb(149,209,251)
---

<Block>
  <Prose>
    **Temporal Extent:** 6 days prior - Present<br />
    **Temporal Resolution:** Daily<br />
    **Spatial Extent:** Alaska<br />
    **Spatial Resolution:** 0.03° x 0.03°<br />
    **Data Type:** Research<br />
    **Data Latency:** Updated Daily
  </Prose>
</Block>

<Block>
  <Prose>
    ## Source Data Product Citation
    Kumar, S.V., C.D. Peters-Lidard, Y. Tian, P.R. Houser, J. Geiger, S. Olden, L. Lighty, J.L. Eastman, B. Doty, P. Dirmeyer, J. Adams, K. Mitchell, E. F. Wood, and J. Sheffield.
  </Prose>
</Block>
```

---

## **📜 License**
This project is **open-source** under the **MIT License**.

---

## **💡 Author**
Developed by NASA VEDA.

---

## **✨ Conclusion**
This script **seamlessly** converts **DOCX → MDX** while **preserving metadata, structure, and formatting**. 🚀  
If you found this useful, feel free to **contribute** or **star** ⭐ the repo! 🚀

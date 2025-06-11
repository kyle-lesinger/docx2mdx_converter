# **DOCX to MDX Converter for VEDA Datasets**

## **📌 Overview**
This Python script converts structured **DOCX files** into **MDX (Markdown + JSX)** format, preserving **metadata, content structure, and color formatting** while ensuring **correct spacing, indentation, and color conversions**.

This is specific for NASA VEDA information. Use file ```template/test_LIS.docx``` as the template and then fill ```template/test_LIS.docx``` in the appropriate information for each section. 

### **Features:**
- ✅ **Extracts** metadata, structured tables, and formatted text from DOCX (use file test_LIS.docx for the proper format)
- ✅ **Handles a dynamic number of layers** (e.g., supporting datasets with varying numbers of layers, not limited to a fixed count).
- ✅ **Converts colors** between **Hex ↔ RGB** if needed
- ✅ **Builds complete MDX content in memory** for efficient single-pass writing.
- ✅ **Ensures clean YAML output** for frontmatter, preventing common formatting issues.



## **📌 Restrictions**
This currently should only be run with a **single landing page collection**. For example, Land Information System - Alaska in ```fill template/test_LIS.docx``` will have four different layers, but will be featured on [VEDA data catalog](https://www.earthdata.nasa.gov/dashboard/data-catalog/global-reanalysis-da) as a single item. In the previous link (for a different dataset), all of the information will be populated and when clicking [Explore Data](https://www.earthdata.nasa.gov/dashboard/exploration?search=global-reanalysis-da&datasets=%5B%5D&taxonomy=%7B%7D) each of the individual layers will be populated based on the information you add. This script will support an infinite number of layers (as long as the same formatting between layers is used). 

---

## **📦 Installation**
### **🔹 Install in new conda environment**
It is not necessary to create a new conda environment due to minimal libraries installed, but a new environment can be created with
```bash
conda env create -f setup/docx2mdx_env.yaml
conda activate docx2mdx
```

### **🔹 Required Dependencies** (no new conda environment)
Ensure you have **Python >=3.7** installed.
The primary dependencies are `python-docx` and `ruamel.yaml`.
Run:
```bash
pip install -r setup/requirements.txt
```
The script uses minimal external libraries, so creating a dedicated Conda environment might not be strictly necessary, but it's good practice for reproducibility.
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
- Extracts DOCX table and prose information
- Converts it into a **structured MDX file**
- Saves into `markdown/` directory

---


### **🔹 1. Color Conversion (Hex ↔ RGB)**
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

### **🔹 2. Converting DOCX file to MDX**
Extracts **table data, metadata, and prose blocks** while preserving formatting.

🔹 **Function:** `convert_docx_to_mdx_path()`
```python
def convert_docx_to_mdx_path(docx_path):
    """
    Converts a .docx file path to .data.mdx in 'converted_markdown'.
    """
```
- Creates `markdown/` folder
- **Renames `.docx` → `.data.mdx`**
- Saves the formatted MDX file

---


### **🔹 3. MDX Content Assembly**
The script assembles the complete MDX content, including YAML frontmatter and all prose blocks, in memory before writing to the output file. This ensures correct structure and ordering.

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

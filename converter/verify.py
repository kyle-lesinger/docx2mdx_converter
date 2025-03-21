#!/usr/bin/env python3

def check_if_colormap_is_valid(colormap):
    #Pulled from https://github.com/NASA-IMPACT/veda-config/blob/develop/admin/config.yml
    valid_colors = ["accent","accent_r","afmhot","afmhot_r","autumn","autumn_r","binary","binary_r","blues","blues_r",
                    "bone","bone_r","brbg","brbg_r","brg","brg_r","bugn","bugn_r","bupu","bupu_r","bwr","bwr_r",
                    "cfastie","cividis","cividis_r","cmrmap","cmrmap_r","cool","cool_r","coolwarm","coolwarm_r",
                    "copper","copper_r","cubehelix","cubehelix_r","dark2","dark2_r","flag","flag_r","gist_earth",
                    "gist_earth_r","gist_gray","gist_gray_r","gist_heat","gist_heat_r","gist_ncar","gist_ncar_r",
                    "gist_rainbow","gist_rainbow_r","gist_stern","gist_stern_r","gist_yarg","gist_yarg_r","gnbu",
                    "gnbu_r","gnuplot","gnuplot2","gnuplot2_r","gnuplot_r","gray","gray_r","greens","greens_r","greys",
                    "greys_r","hot","hot_r","hsv","hsv_r","inferno","inferno_r","jet","jet_r","magma","magma_r","nipy_spectral",
                    "nipy_spectral_r","ocean","ocean_r","oranges","oranges_r","orrd","orrd_r","paired","paired_r",
                    "pastel1","pastel1_r","pastel2","pastel2_r","pink","pink_r","piyg","piyg_r","plasma","plasma_r",
                    "prgn","prgn_r","prism","prism_r","pubu","pubu_r","pubugn","pubugn_r","puor","puor_r","purd",
                    "purd_r","purples","purples_r","rainbow","rainbow_r","rdbu","rdbu_r","rdgy","rdgy_r","rdpu",
                    "rdpu_r","rdylbu","rdylbu_r","rdylgn","rdylgn_r","reds","reds_r","rplumbo","schwarzwald",
                    "seismic","seismic_r","set1","set1_r","set2","set2_r","set3","set3_r","spectral","spectral_r",
                    "spring","spring_r","summer","summer_r","tab10","tab10_r","tab20","tab20_r","tab20b","tab20b_r",
                    "tab20c","tab20c_r","terrain","terrain_r","twilight","twilight_r","twilight_shifted","twilight_shifted_r",
                    "viridis","viridis_r","winter","winter_r","wistia","wistia_r","ylgn","ylgn_r","ylgnbu","ylgnbu_r",
                    "ylorbr","ylorbr_r","ylorrd","ylorrd_r",None]
    if colormap not in valid_colors:
        raise ValueError(f"Invalid colormap: {colormap}. \n\nPlease choose from the list of {valid_colors}.")
    return colormap

        
    

def check_if_projection_is_valid(projection):
    #Pulled from https://github.com/NASA-IMPACT/veda-config/blob/develop/admin/config.yml
    valid_projection = ["albers","equalEarth","equirectangular","lambertConformalConic","mercator","naturalEarth","winkelTripel",
                      "globe","polarNorth","polarSouth",]
    if projection not in valid_projection:
        raise ValueError(f"Invalid projection: {projection}. Please choose from the list of {valid_projection}.")
    return projection   
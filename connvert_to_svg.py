import os
import subprocess
import shutil

def convert_png_to_svg(input_dir="extracted_characters", output_dir="vector_characters", output_svg="svgs/final_font.svg"):
    
    os.makedirs(output_dir, exist_ok=True)
    glyphs = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            pgm_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.pgm")
            svg_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.svg")
            subprocess.run(["convert", input_path, "-threshold", "50%", pgm_path])
            subprocess.run(["potrace", "-s", pgm_path, "-o", svg_path])
            
            with open(svg_path, "r") as svg_file:
                svg_content = svg_file.read()
                if 'd="' in svg_content:
                    start_index = svg_content.find('d="') + 3
                    end_index = svg_content.find('"', start_index)
                    path_data = svg_content[start_index:end_index]
                    char_name = os.path.splitext(filename)[0].lower()
                    glyphs.append((char_name, path_data))
    
    svg_header = '''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
    <metadata>
    Created by FontForge 20200511 at Fri Apr 28 08:44:13 2023
    By convertio
    Your name font Typeline Studio 2020. All Rights Reserved
    </metadata>
    <defs>
    <font id="AlphaBrights" horiz-adv-x="388">
    <font-face 
        font-family="Alpha Brights"
        font-weight="400"
        font-stretch="normal"
        units-per-em="1000"
        panose-1="2 0 5 0 0 0 0 0 0 0"
        ascent="800"
        descent="-200"
        x-height="289"
        cap-height="993"
        bbox="-1339.01 -772.84 2192.52 1201.05"
        underline-thickness="50"
        underline-position="-75"
        unicode-range="U+001D-E007"
    />
    <missing-glyph horiz-adv-x="500" />
    '''
    
    svg_content = svg_header
    for char_name, path_data in glyphs:
        svg_content += f'<glyph glyph-name="{char_name.lower()}" unicode="{char_name.lower()}" horiz-adv-x="1000" d="{path_data}" />'
        
    svg_footer = '''
    </font>
    </defs>
    </svg>
    '''

    svg_content += svg_footer
    with open(output_svg, "w") as final_svg_file:
        final_svg_file.write(svg_content)

    print(f"Converted PNG images to SVG and saved in '{output_svg}'.")
    shutil.rmtree("extracted_characters")
    shutil.rmtree("vector_characters")
    subprocess.run(["fontforge", "-script", "ttf_conversion.py"])


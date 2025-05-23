import fontforge
import os
os.makedirs("fonts", exist_ok=True)
font = fontforge.open("svgs/final_font.svg")
font.fontname = "Custom_Font"
font.familyname = "Custom_Font"
font.fullname = "Custom_Font"
font.weight = "Regular"
font.generate("fonts/Custom_Font.ttf")

print("Font converted to TTF format successfully!")

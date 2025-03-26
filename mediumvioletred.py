#!/usr/bin/env fontforge
import fontforge
import os

# Prompt the user to enter a font name via the console
font_name = input("Enter the font name: ").strip()

# Create a new font with the provided name
font = fontforge.font()
font.fontname = font_name
font.fullname = font_name
font.familyname = font_name

# Folder containing the SVG glyphs
glyph_folder = "glyphs"

# Process each SVG file in the glyph folder
for filename in os.listdir(glyph_folder):
    if filename.lower().endswith(".svg"):
        # Use the file name (without extension) to determine the Unicode codepoint.
        name = os.path.splitext(filename)[0]
        try:
            if len(name) == 1:
                codepoint = ord(name)
            else:
                # If filenames are in hex (e.g., "0041.svg"), convert them to an integer codepoint.
                codepoint = int(name, 16)
        except Exception:
            print(f"Skipping file {filename}: cannot determine Unicode codepoint.")
            continue

        # Create a new glyph for the codepoint and import its outline
        glyph = font.createChar(codepoint)
        glyph.importOutlines(os.path.join(glyph_folder, filename))
        glyph.correctDirection()  # Ensure the outline direction is correct

        # Compute the bounding box of the imported outline
        bbox = glyph.boundingBox()  # Returns (xMin, yMin, xMax, yMax)
        if bbox:
            xMin, yMin, xMax, yMax = bbox
            # Define a margin (50 units on each side, total margin = 100)
            margin = 100
            # Adjust the left side bearing so that the left margin becomes 50 units.
            glyph.left_side_bearing = int(50 - xMin)
            # Set the glyph width to the outline width plus the defined margin.
            glyph.width = int((xMax - xMin) + margin)
        else:
            # If bounding box cannot be determined, fall back to a default width.
            glyph.width = 1000

# Generate the TrueType font file with the font name
output_file = f"{font_name}.ttf"
font.generate(output_file)
print(f"Successfully generated {output_file}")

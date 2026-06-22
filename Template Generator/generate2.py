from dataclasses import dataclass
import numpy as np
import svgwrite

paper_width = 210
paper_height = 297

# Number of templates per a4 sheet
number_of_templates = 3

template_width = paper_width/number_of_templates
template_height = paper_height

min_wing_length = 27
min_tail_length = 27
min_body_length = 13.5
maximum_segments = 5

@dataclass
class Template:
    wing_length: float
    tail_length: float

templates = []

th2 = template_height/2
for wing in np.linspace(min_body_length, th2-min_wing_length, maximum_segments):
    for tail in np.linspace(min_body_length, th2-min_tail_length, maximum_segments):
        templates.append(Template(th2-wing, th2-tail))

for i, page_templates in enumerate(np.array_split(templates, np.ceil(len(templates)/number_of_templates))):
    dwg = svgwrite.Drawing(f"template_{i}.svg", size=(f"{paper_width}mm", f"{paper_height}mm"), viewBox=f"0 0 {paper_width} {paper_height}")

    for j, template in enumerate(page_templates):
        print(template)
        strokes = "5,5"
        offset = j*template_width

        dwg.add(dwg.rect((offset, 0), (template_width, template_height), fill="white", stroke="black"))
        dwg.add(dwg.line((offset, 0), (offset, template_height), stroke="black"))

        middle = offset+template_width/2
        dwg.add(dwg.line((offset+template_width/4, 0), (offset+template_width/4, template.wing_length), stroke="black"))
        dwg.add(dwg.line((offset+3*template_width/4, 0), (offset+3*template_width/4, template.wing_length), stroke="black"))
        dwg.add(dwg.text(f"{template.wing_length}", insert=(middle+2, template.wing_length/2), font_size="6px"))

        dwg.add(dwg.line((middle, 0), (middle, template.wing_length), stroke="black"))
        dwg.add(dwg.line((offset, template.wing_length), (offset+template_width, template.wing_length), stroke="black", stroke_dasharray=strokes))

        body_length = template_height-(template.wing_length+template.tail_length)
        after_body = body_length+template.wing_length
        quarter = template_width/4
        dwg.add(dwg.line((offset, after_body), (offset+quarter, after_body), stroke="black"))
        dwg.add(dwg.line((offset+quarter, after_body), (offset+quarter, after_body+template.tail_length), stroke="black", stroke_dasharray=strokes))
        dwg.add(dwg.line((offset+quarter*3, after_body), (offset+quarter*4, after_body), stroke="black"))
        dwg.add(dwg.line((offset+quarter*3, after_body), (offset+quarter*3, after_body+template.tail_length), stroke="black", stroke_dasharray=strokes))
        dwg.add(dwg.text(f"{template.tail_length}mm", insert=(offset+quarter+2, after_body+template.tail_length/2), font_size="6px"))

        dwg.add(dwg.line((offset, template_height-10), (offset+quarter*4, template_height-10), stroke="black", stroke_dasharray=strokes))

    dwg.save()

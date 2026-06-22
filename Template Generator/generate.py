from dataclasses import dataclass
import numpy as np
import svgwrite

paper_width = 210
paper_height = 297

# Number of templates per a4 sheet
number_of_templates = 3

template_width = paper_width/number_of_templates
template_height = paper_height

min_wing_length = 40
min_tail_length = 40
maximum_segments = 7
segment_size = (template_height-min_wing_length-min_tail_length)/maximum_segments

@dataclass
class Template:
    body_length: float
    wing_length: float
    tail_length: float

templates = []

for body_segments in range(1, maximum_segments+1):
    body_length = segment_size*np.arange(1, body_segments+1)
    wing_length = min_wing_length+(maximum_segments-body_segments)*segment_size
    tail_length = template_height-(body_length+wing_length)
    
    for b, t in zip(body_length, tail_length):
        templates.append(Template(b, wing_length, t))

for i, page_templates in enumerate(np.array_split(templates, np.ceil(len(templates)/number_of_templates))):
    dwg = svgwrite.Drawing(f"template_{i}.svg", size=(f"{paper_width}mm", f"{paper_height}mm"), viewBox=f"0 0 {paper_width} {paper_height}")


    for j, template in enumerate(page_templates):
        strokes = "5,5"
        offset = j*template_width

        dwg.add(dwg.rect((offset, 0), (template_width, template_height), fill="white", stroke="black"))

        dwg.add(dwg.line((offset, 0), (offset, template_height), stroke="black"))
        
        middle = offset+template_width/2
        dwg.add(dwg.line((middle, 0), (middle, template.wing_length), stroke="black"))
        dwg.add(dwg.line((offset, template.wing_length), (offset+template_width, template.wing_length), stroke="black", stroke_dasharray=strokes))

        after_body = template.body_length+template.wing_length
        quarter = template_width/4
        dwg.add(dwg.line((offset, after_body), (offset+quarter, after_body), stroke="black"))
        dwg.add(dwg.line((offset+quarter, after_body), (offset+quarter, after_body+template.tail_length), stroke="black", stroke_dasharray=strokes))
        dwg.add(dwg.line((offset+quarter*3, after_body), (offset+quarter*4, after_body), stroke="black"))
        dwg.add(dwg.line((offset+quarter*3, after_body), (offset+quarter*3, after_body+template.tail_length), stroke="black", stroke_dasharray=strokes))

    dwg.save()

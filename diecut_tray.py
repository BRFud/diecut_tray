#!/usr/bin/env python3
"""
Simple python to create a tray die‑cut SVG file with double-folds for sides, flaps and base insert, intended for cutting cardstock on a laser cutting machine.
Original intent was to make some small but robust trays from thin card for holding rocks and mineral specimins. I could not find a good free die-cut pattern online.
The base insert (blue box in the resulting SVG) should be repositioned so as not to overlap with the rest of the die cut in your laser cutting software.
License: MIT
"""
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
import math


# ------------------------------------------------------------------
# Default values – they can be overridden on the command line
# ------------------------------------------------------------------
DEFAULT_WIDTH   = 60.0
DEFAULT_DEPTH   = 75.0
DEFAULT_HEIGHT  = 30.0
DEFAULT_THICK   = 0.1


def create_diecut_tray_svg(base_width, base_depth, wall_height, paper_thickness, filename="diecut_tray.svg"):
    """
    Generate SVG diecut pattern for a tray with double-fold walls, flaps, and bottom insert
    """

    # SVG dimensions

    page_width = 210
    page_height = 297
  
    base_x = [-base_width/2, base_width/2, base_width/2, -base_width/2]
    base_y = [-base_depth/2, -base_depth/2, base_depth/2, base_depth/2]
    
    a1=(-base_width/2,-base_depth/2)
    a2=(base_width/2,-base_depth/2)
    a3=(base_width/2,base_depth/2)
    a4=(-base_width/2,base_depth/2)
  
    #tray bottom insert
    bottom_insert_shrink=0.4
    bottom_insert1=(a1[0]+bottom_insert_shrink,a1[1]+bottom_insert_shrink)
    bottom_insert2=(a2[0]-bottom_insert_shrink,a2[1]+bottom_insert_shrink)
    bottom_insert3=(a3[0]-bottom_insert_shrink,a3[1]-bottom_insert_shrink)
    bottom_insert4=(a4[0]+bottom_insert_shrink,a4[1]-bottom_insert_shrink)
    
    b1=(a1[0],a1[1]-wall_height)
    b2=(a2[0],b1[1])
    b3=(a2[0],a3[1]+wall_height)
    #b4=(,)
    
    c1=(b1[0]+paper_thickness,b1[1]-2*paper_thickness)
    c2=(b2[0]-paper_thickness,c1[1])
    #c3=(,)
    #c4=(,)
      
    d1=(c1[0]+0.5,c1[1]-wall_height+paper_thickness)
    d2=(c2[0]-0.5,d1[1])
    #d3=(,)
    #d4=(,)
       
    e1=(d1[0]+wall_height/10,d1[1]-base_depth/10)
    e2=(d2[0]-wall_height/10,e1[1])
    #e3=(,)
    #e4=(,)
       
    #f1=(b1[0]-wall_height+2*paper_thickness,b1[1]+2*paper_thickness)
    f2=(b2[0]+wall_height,b1[1]+wall_height/10)
    f3=(f2[0],a3[1]+wall_height-wall_height/10)
    #f4=(,)
       
    #g1=(a1[0]-wall_height,a1[1])
    g2=(a2[0]+wall_height,a1[1])
    g3=(a2[0]+wall_height,a3[1])
    #g4=(g1[0],a3[1])
       
    #h1=(g1[0]-2*paper_thickness,g1[1]+paper_thickness)
    h2=(g2[0]+2*paper_thickness,g2[1]+paper_thickness)
    h3=(h2[0],g3[1]-paper_thickness)
    #h4=(,)
       
    #i1=(,)
    i2=(h2[0]+wall_height/10,f2[1])
    i3=(i2[0],f3[1])
    #i4=(,)

    #j1=(,)
    j2=(h2[0]+wall_height-paper_thickness,h2[1])
    j3=(j2[0],h3[1])
    #j4=(,)
       
    #k1=(,)
    k2=(j2[0]-wall_height/10,f2[1])
    k3=(k2[0],i3[1])
    #k4=(,)
       
    #l1=(,)
    l2=(j2[0]+base_width/10,j2[1]+wall_height/10)
    l3=(l2[0],j3[1]-wall_height/10)
    #l4=(,)
    #e1=(d1[0]+wall_height/10,d1[1]-base_depth/10)
    #e2=(d2[0]-wall_height/10,e1[1])
  
    m2=(g2[0],g2[1]-wall_height/10)
    m3=(g2[0],g3[1]+wall_height/10)
  
       
    # Create SVG root element
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'width': f'{page_width}mm',
        'height': f'{page_height}mm',
        'viewBox': f'0 0 {page_width} {page_height}',
    })
    
    # Add CSS styles
    style = ET.SubElement(svg, 'style')
    style.text = """
        .cut2 { stroke: blue; stroke-width: 0.1;  fill: none;}
        .fold { stroke: green; stroke-width: 0.1; fill: none;}
        .cut { stroke: red; stroke-width: 0.1;  fill: none;}
        .label { font-family: Arial, sans-serif; font-size: 12px; }
    """

    # Create a centered group element
    center_group = ET.SubElement(svg, 'g', {
        'transform': f'translate({page_width/2}, {page_height/2})'
    })

    # Draw base rectangle
    # Create path data manually
    path_data = f'M {a1[0]},{a1[1]} L {a2[0]},{a2[1]} L {a3[0]},{a3[1]} L {a4[0]},{a4[1]} Z'

    # Draw the polygon
    polygon = ET.SubElement(center_group, 'path', {
        'd': path_data,
        'class': 'fold'
    })

    # Draw base rectangle
    # Create path data manually
    path_data = f'M {bottom_insert1[0]},{bottom_insert1[1]} L {bottom_insert2[0]},{bottom_insert2[1]} L {bottom_insert3[0]},{bottom_insert3[1]} L {bottom_insert4[0]},{bottom_insert4[1]} Z'

    # Draw the polygon
    polygon = ET.SubElement(center_group, 'path', {
        'd': path_data,
        'class': 'cut2',
        'transform': 'rotate(90, 0, 0)'  # Rotate 180° around center (0,0)
    })

    # FOLDS
    # Array of line segments
    lines = [
        (a1, b1),(b1, b2),(b2, a2),(c1,c2),(d1,d2),
        (g2, g3),(h2, h3),(j2, j3),(h2, j2),(h3, j3),
    ]

    # Create separate path elements for each line
    for a, b in lines:
        line_path = f'M {a[0]},{a[1]} L {b[0]},{b[1]}'
        line = ET.SubElement(center_group, 'path', {
            'd': line_path,
            'class': 'fold'
        })
    
    # Create separate path elements for each line
    for a, b in lines:
        line_path = f'M {a[0]},{a[1]} L {b[0]},{b[1]}'
        line = ET.SubElement(center_group, 'path', {
            'd': line_path,
            'class': 'fold',
            'transform': 'rotate(180, 0, 0)'  # Rotate 180° around center (0,0)
        })
    
    # CUTS
    # Array of line segments
    lines = [
        (b1, c1),(c1, d1),(d1, e1),(e1, e2),(e2, d2),(d2,c2),(c2,b2),(b2,f2),(f2, m2),(m2, a2),(g2, h2),(h2, i2),(i2, k2),(k2, j2),
        (j2, l2),(l2, l3),(l3, j3),(j3,k3),(k3,i3),(i3, h3),(h3, g3),(a3,m3),(m3, f3),(f3, b3),
        (a2, g2),(a3, g3)
    ]

    # Create separate path elements for each line
    for a, b in lines:
        line_path = f'M {a[0]},{a[1]} L {b[0]},{b[1]}'
        line = ET.SubElement(center_group, 'path', {
            'd': line_path,
            'class': 'cut'
        })

    
    # Create separate path elements for each line
    for a, b in lines:
        line_path = f'M {a[0]},{a[1]} L {b[0]},{b[1]}'
        line = ET.SubElement(center_group, 'path', {
            'd': line_path,
            'class': 'cut',
            'transform': 'rotate(180, 0, 0)'  # Rotate 180° around center (0,0)
        })

    # Pretty print the XML
    rough_string = ET.tostring(svg, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Write to file
    with open(filename, 'w') as f:
        f.write(pretty_xml)
    
    print(f"SVG file '{filename}' has been created successfully!")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a die‑cut SVG for a paper tray."
    )
    parser.add_argument("--width", dest="width",
                        type=float, default=DEFAULT_WIDTH,
                        help=f"Tray width in mm (default {DEFAULT_WIDTH})")
    parser.add_argument("--depth", dest="depth",
                        type=float, default=DEFAULT_DEPTH,
                        help=f"Tray depth in mm (default {DEFAULT_DEPTH})")
    parser.add_argument("--height", dest="height",
                        type=float, default=DEFAULT_HEIGHT,
                        help=f"Tray height in mm (default {DEFAULT_HEIGHT})")
    parser.add_argument("--thick", dest="thick",
                        type=float, default=DEFAULT_THICK,
                        help=f"Paper thickness in mm (default {DEFAULT_THICK})")
    parser.add_argument("--output", dest="output",
                        default="diecut_tray.svg",
                        help="Name of the output SVG file (default 'diecut_tray.svg')")

    return parser.parse_args()


def main():
    args = parse_args()

    # Call the function with the (possibly overridden) values
    create_diecut_tray_svg(
        base_width=args.width,
        base_depth=args.depth,
        wall_height=args.height,
        paper_thickness=args.thick,
        filename=args.output
    )


if __name__ == "__main__":
    main()

import ezdxf
from ezdxf.math import Vec2 as Vector
from math import pi, cos, sin

doc = ezdxf.new(dxfversion="R2010")

# Define layers with colors (AutoCAD ACI colors)
layers = {
    "WALLS": 1,         # red
    "FURNITURE": 3,     # green
    "DOORS": 4,         # cyan
    "WINDOWS": 5,       # blue
    "TEXT": 7,          # white/black
    "DIMENSIONS": 2,    # yellow
    "HATCH": 8          # magenta
}
for layer, color in layers.items():
    doc.layers.new(name=layer, dxfattribs={"color": color})

msp = doc.modelspace()

# Helper functions
def draw_wall(x1, y1, x2, y2, thickness=200, layer="WALLS"):
    """Draw double line wall as LWPolyline"""
    v1 = Vector(x1, y1)
    v2 = Vector(x2, y2)
    direction = (v2 - v1).normalize()
    offset = direction.orthogonal() * thickness / 2
    pts = [
        v1 - offset,
        v2 - offset,
        v2 + offset,
        v1 + offset,
    ]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    # Add hatch inside walls
    hatch = msp.add_hatch(color=layers["HATCH"], dxfattribs={"layer": "HATCH"})
    hatch.paths.add_polyline_path(pts)

def draw_door(x, y, width=900, swing=900, rotation=0, layer="DOORS"):
    """Draw door with arc swing"""
    # Door line
    msp.add_line((x, y), (x + width, y), dxfattribs={"layer": layer})
    # Arc swing
    center = (x, y)
    start_angle = 0
    end_angle = 90
    if rotation != 0:
        # Rotate door line and arc around (x,y)
        # Rotation in degrees counterclockwise
        from math import radians
        angle = radians(rotation)
        def rotate_point(px, py):
            dx, dy = px - x, py - y
            rx = dx * cos(angle) - dy * sin(angle) + x
            ry = dx * sin(angle) + dy * cos(angle) + y
            return rx, ry
        p1 = (x + width, y)
        p1r = rotate_point(*p1)
        msp.add_line((x, y), p1r, dxfattribs={"layer": layer})
        # Arc points for swing
        arc_center = (x, y)
        arc = msp.add_arc(center=arc_center, radius=swing,
                          start_angle=rotation, end_angle=rotation + 90,
                          dxfattribs={"layer": layer})
    else:
        msp.add_arc(center=center, radius=swing,
                    start_angle=start_angle, end_angle=end_angle,
                    dxfattribs={"layer": layer})

def draw_window(x, y, width=1200, height=1200, layer="WINDOWS"):
    """Draw window as rectangle with panes"""
    pts = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    # Cross panes
    msp.add_line((x + width/2, y), (x + width/2, y + height), dxfattribs={"layer": layer})
    msp.add_line((x, y + height/2), (x + width, y + height/2), dxfattribs={"layer": layer})

def add_text(text, pos, height=250, layer="TEXT"):
    msp.add_text(text, dxfattribs={"height": height, "layer": layer}).set_pos(pos)

def draw_dimension(base_x, base_y, start_point, end_point, offset=300, horizontal=True):
    """Draw a simple dimension line with arrows and text"""
    arrow_size = 100
    # Calculate dimension line points
    if horizontal:
        dim_line_start = (start_point[0], base_y - offset)
        dim_line_end = (end_point[0], base_y - offset)
        # Dimension text
        dist = abs(end_point[0] - start_point[0])
        text_pos = ((start_point[0] + end_point[0]) / 2, base_y - offset - 200)
    else:
        dim_line_start = (base_x - offset, start_point[1])
        dim_line_end = (base_x - offset, end_point[1])
        dist = abs(end_point[1] - start_point[1])
        text_pos = (base_x - offset - 800, (start_point[1] + end_point[1]) / 2)

    # Dimension line
    msp.add_line(dim_line_start, dim_line_end, dxfattribs={"layer": "DIMENSIONS"})
    # Arrows (simple lines)
    if horizontal:
        # Left arrow
        msp.add_line(
            (dim_line_start[0], dim_line_start[1] + arrow_size/2),
            (dim_line_start[0], dim_line_start[1] - arrow_size/2),
            dxfattribs={"layer": "DIMENSIONS"})
        # Right arrow
        msp.add_line(
            (dim_line_end[0], dim_line_end[1] + arrow_size/2),
            (dim_line_end[0], dim_line_end[1] - arrow_size/2),
            dxfattribs={"layer": "DIMENSIONS"})
    else:
        # Bottom arrow
        msp.add_line(
            (dim_line_start[0] - arrow_size/2, dim_line_start[1]),
            (dim_line_start[0] + arrow_size/2, dim_line_start[1]),
            dxfattribs={"layer": "DIMENSIONS"})
        # Top arrow
        msp.add_line(
            (dim_line_end[0] - arrow_size/2, dim_line_end[1]),
            (dim_line_end[0] + arrow_size/2, dim_line_end[1]),
            dxfattribs={"layer": "DIMENSIONS"})

    # Text
    add_text(f"{dist/1000:.2f} m", text_pos, height=200, layer="DIMENSIONS")

def draw_stair(x, y, step_width=1000, step_height=300, steps=10, layer="FURNITURE"):
    """Draw a stair with steps as rectangles ascending upward"""
    for i in range(steps):
        start_x = x + i * step_width
        start_y = y + i * step_height
        pts = [
            (start_x, start_y),
            (start_x + step_width, start_y),
            (start_x + step_width, start_y + step_height),
            (start_x, start_y + step_height),
        ]
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    add_text("Stairs", (x + steps*step_width/2 - 800, y + steps*step_height + 200), layer=layer)

def draw_furniture(x, y, w, h, label, layer="FURNITURE"):
    """Draw a simple rectangle furniture and label"""
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    add_text(label, (x + 100, y + h/2 - 100), layer=layer)

def draw_3bhk_floor_plan(base_x, base_y, label):
    width = 9000
    height = 6000
    wall_thickness = 200

    # Outer walls (rectangle)
    draw_wall(base_x, base_y, base_x + width, base_y, thickness=wall_thickness)
    draw_wall(base_x + width, base_y, base_x + width, base_y + height, thickness=wall_thickness)
    draw_wall(base_x + width, base_y + height, base_x, base_y + height, thickness=wall_thickness)
    draw_wall(base_x, base_y + height, base_x, base_y, thickness=wall_thickness)

    # Inner walls (some divisions for rooms)
    # Vertical walls
    draw_wall(base_x + 3000, base_y, base_x + 3000, base_y + 6000, thickness=wall_thickness)
    draw_wall(base_x + 6000, base_y, base_x + 6000, base_y + 4000, thickness=wall_thickness)
    # Horizontal walls
    draw_wall(base_x, base_y + 4000, base_x + 6000, base_y + 4000, thickness=wall_thickness)
    draw_wall(base_x + 3000, base_y + 2000, base_x + 6000, base_y + 2000, thickness=wall_thickness)

    # Doors (with rotation where needed)
    draw_door(base_x + 1000, base_y, width=900)  # main door bottom wall
    draw_door(base_x + 3000, base_y + 1000, width=900, rotation=90)  # vertical wall door
    draw_door(base_x + 3000, base_y + 3000, width=900, rotation=90)  # vertical wall door
    draw_door(base_x + 6000, base_y + 1000, width=900, rotation=90)  # vertical wall door
    draw_door(base_x + 4500, base_y + 4000, width=900)  # horizontal wall door

    # Windows
    draw_window(base_x + 500, base_y + 2500)
    draw_window(base_x + 7500, base_y + 2500)
    draw_window(base_x + 4000, base_y + 5800)

    # Stair (bottom left corner inside)
    draw_stair(base_x + 1000, base_y + 4200, steps=8)

    # Furniture (beds in bedrooms)
    draw_furniture(base_x + 400, base_y + 100, 2500, 1500, "Bed")
    draw_furniture(base_x + 3200, base_y + 4200, 2500, 1500, "Bed")
    draw_furniture(base_x + 6200, base_y + 100, 2200, 1500, "Bed")
    # Sofa in hall
    draw_furniture(base_x + 3200, base_y + 2500, 2200, 1500, "Sofa")
    # Kitchen counter
    draw_furniture(base_x + 6200, base_y + 4200, 2200, 1200, "Kitchen Counter")

    # Dimensions
    draw_dimension(base_x, base_y, (base_x, base_y), (base_x + width, base_y), offset=400)  # width
    draw_dimension(base_x, base_y, (base_x, base_y), (base_x, base_y + height), offset=400, horizontal=False)  # height

    # Label floor
    add_text(label, (base_x + width/2 - 1200, base_y - 600), height=400)

# Draw ground floor at origin
draw_3bhk_floor_plan(0, 0, "Ground Floor")

# Draw first floor shifted right (10,000 mm)
draw_3bhk_floor_plan(10000, 0, "First Floor")

# Front Elevation below floors
fe_base_x = 0
fe_base_y = -7000
# Outer walls rectangle ground floor elevation
msp.add_lwpolyline([
    (fe_base_x, fe_base_y),
    (fe_base_x + 9000, fe_base_y),
    (fe_base_x + 9000, fe_base_y - 3000),
    (fe_base_x, fe_base_y - 3000),
    (fe_base_x, fe_base_y)
], close=True, dxfattribs={"layer": "WALLS", "color": layers["WALLS"]})

# First floor walls elevation
msp.add_lwpolyline([
    (fe_base_x, fe_base_y - 3000),
    (fe_base_x + 9000, fe_base_y - 3000),
    (fe_base_x + 9000, fe_base_y - 6000),
    (fe_base_x, fe_base_y - 6000),
    (fe_base_x, fe_base_y - 3000)
], close=True, dxfattribs={"layer": "WALLS", "color": layers["WALLS"]})

# Roof - simple gable
msp.add_line((fe_base_x, fe_base_y - 6000), (fe_base_x + 4500, fe_base_y - 7000), dxfattribs={"layer": "WALLS"})
msp.add_line((fe_base_x + 9000, fe_base_y - 6000), (fe_base_x + 4500, fe_base_y - 7000), dxfattribs={"layer": "WALLS"})

add_text("Front Elevation", (fe_base_x + 3500, fe_base_y - 7500), height=400)

# Windows in elevation (3 per floor)
for i in range(3):
    wx = fe_base_x + 1500 + i * 2500
    wy_g = fe_base_y - 1500
    wy_f = fe_base_y - 4500
    # Ground floor window
    msp.add_lwpolyline([
        (wx, wy_g - 300),
        (wx + 1200, wy_g - 300),
        (wx + 1200, wy_g + 300),
        (wx, wy_g + 300),
        (wx, wy_g - 300)
    ], close=True, dxfattribs={"layer": "WINDOWS"})
    # First floor window
    msp.add_lwpolyline([
        (wx, wy_f - 300),
        (wx + 1200, wy_f - 300),
        (wx + 1200, wy_f + 300),
        (wx, wy_f + 300),
        (wx, wy_f - 300)
    ], close=True, dxfattribs={"layer": "WINDOWS"})

# Section view right side
sec_base_x = 10000
sec_base_y = -7000

# Ground floor section walls
msp.add_lwpolyline([
    (sec_base_x, sec_base_y),
    (sec_base_x + 9000, sec_base_y),
    (sec_base_x + 9000, sec_base_y - 3000),
    (sec_base_x, sec_base_y - 3000),
    (sec_base_x, sec_base_y)
], close=True, dxfattribs={"layer": "WALLS"})

# First floor section walls
msp.add_lwpolyline([
    (sec_base_x, sec_base_y - 3000),
    (sec_base_x + 9000, sec_base_y - 3000),
    (sec_base_x + 9000, sec_base_y - 6000),
    (sec_base_x, sec_base_y - 6000),
    (sec_base_x, sec_base_y - 3000)
], close=True, dxfattribs={"layer": "WALLS"})

# Floor slab line
msp.add_line((sec_base_x, sec_base_y - 3000), (sec_base_x + 9000, sec_base_y - 3000), dxfattribs={"layer": "WALLS"})
# Roof slab line
msp.add_line((sec_base_x, sec_base_y - 6000), (sec_base_x + 9000, sec_base_y - 6000), dxfattribs={"layer": "WALLS"})

add_text("Section View", (sec_base_x + 3500, sec_base_y - 7500), height=400)

# Save DXF file
filename = "3BHK_2Story_House_Architectural_Enhanced.dxf"
doc.saveas(filename)
print(f"✅ Enhanced DXF file '{filename}' created successfully.")

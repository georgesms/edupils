import asyncio
from js import document
from pyodide import create_proxy

def draw_rect(x, y, width, height, color='blue'):
    canvas = document.getElementById('myCanvas')
    ctx = canvas.getContext('2d')
    ctx.fillStyle = color
    ctx.fillRect(x, y, width, height)

def draw_triangle(base_x, base_y, base_width, height, color='red'):
    canvas = document.getElementById('myCanvas')
    ctx = canvas.getContext('2d')
    
    ctx.beginPath()
    ctx.moveTo(base_x, base_y)
    ctx.lineTo(base_x + base_width / 2, base_y - height)
    ctx.lineTo(base_x + base_width, base_y)
    ctx.closePath()
    
    ctx.fillStyle = color
    ctx.fill()

# New function to draw a circle
def draw_circle(center_x, center_y, radius, color='green'):
    canvas = document.getElementById('myCanvas')  # Access the canvas DOM element by its ID.
    ctx = canvas.getContext('2d')  # Get the 2D drawing context of the canvas.
    
    ctx.beginPath()  # Begin a new path for the circle.
    ctx.arc(center_x, center_y, radius, 0, 2 * 3.14159)  # Draw the circle path.
    ctx.fillStyle = color  # Set the fill color for the circle.
    ctx.fill()  # Fill the circle with the specified color.

async def animate():
    x = 0
    y = 50
    width = 100
    height = 50
    while x < 300:
        canvas = document.getElementById('myCanvas')
        ctx = canvas.getContext('2d')
        ctx.clearRect(0, 0, canvas.width, canvas.height)

        draw_rect(x, y, width, height)  # Draw the rectangle.
        draw_triangle(x + 50, y + 100, 60, 30)  # Example of drawing a triangle.
        draw_circle(x + 50, y - 30, 25)  # Example of drawing a circle.

        x += 5
        await asyncio.sleep(0.1)


def draw_line(start_x, start_y, end_x, end_y, color='black', width=1, pattern='solid'):
    canvas = document.getElementById('myCanvas')
    ctx = canvas.getContext('2d')
    
    ctx.beginPath()
    ctx.moveTo(start_x, start_y)
    ctx.lineTo(end_x, end_y)
    
    ctx.strokeStyle = color
    ctx.lineWidth = width
    
    # Set the line pattern
    if pattern == 'dashed':
        ctx.setLineDash([5, 5])
    elif pattern == 'dotted':
        ctx.setLineDash([1, 5])
    else:
        ctx.setLineDash([])  # Solid line
    
    ctx.stroke()

def draw_parabola(a, b, c, start_x, end_x, step=0.1, color='purple', width=1, pattern='solid'):
    canvas = document.getElementById('myCanvas')
    ctx = canvas.getContext('2d')
    
    ctx.beginPath()
    
    for x in range(int((end_x - start_x) / step)):
        x_val = start_x + x * step
        y_val = a * x_val**2 + b * x_val + c
        if x == 0:
            ctx.moveTo(x_val, y_val)
        else:
            ctx.lineTo(x_val, y_val)
    
    ctx.strokeStyle = color
    ctx.lineWidth = width
    
    # Set the line pattern
    if pattern == 'dashed':
        ctx.setLineDash([5, 5])
    elif pattern == 'dotted':
        ctx.setLineDash([1, 5])
    else:
        ctx.setLineDash([])  # Solid line
    
    ctx.stroke()

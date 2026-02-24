from PIL import Image
import numpy as np

size = 7

# Positions
positions = {
    "center": (3, 3),
    "top_left": (1, 1),
    "top_right": (1, 5),
    "middle_left": (3, 1),
    "middle_right": (3, 5),
    "bottom_left": (5, 1),
    "bottom_right": (5, 5),
}

# Dice definitions
dice = {
    1: ["center"],
    2: ["top_left", "bottom_right"],
    3: ["top_left", "center", "bottom_right"],
    4: ["top_left", "top_right", "bottom_left", "bottom_right"],
    5: ["top_left", "top_right", "center", "bottom_left", "bottom_right"],
    6: ["top_left", "middle_left", "bottom_left",
        "top_right", "middle_right", "bottom_right"],
}

def draw_dot(img, x, y):
    # Make a small 3x3 square for each dot
    img[x,y]=255

def create_dice_face(dots):
    img = np.zeros((size, size), dtype=np.uint8)

    for dot in dots:
        x, y = positions[dot]
        draw_dot(img, x, y)

    return img

# Generate all dice
for i in range(7):
    if i>0:
        arr = create_dice_face(dice[i])
    else:
        arr = create_dice_face([])

    img = Image.fromarray(arr, mode='L')

    # Enlarge for visibility
    # img = img.resize((300, 300), Image.NEAREST)

    img.save(f"dice_{i}.png")

print("All 5x5 dice generated!")
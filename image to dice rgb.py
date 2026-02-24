from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None
size = 14  # larger dice blocks for better detail
path = r"C:\Users\Amine Khalil\Documents\Python\image to dice\input\enhanced.jpg"

# Open image in RGB
image = Image.open(path).convert("RGB")

# Resize to multiple of size
width, height = image.size
width -= width % size
height -= height % size
image = image.resize((width, height))

# Load dice images (assume white dots on black background)
dice = {i: Image.open(f"dice_{i}.png").convert("L").resize((size, size)) for i in range(1,7)}
dice_arrays = {i: np.array(dice[i])/255.0 for i in range(1,7)}  # normalize 0-1

# Convert input to array
img_array = np.array(image)

# Prepare output
output_array = np.zeros_like(img_array)

# Function to compute the "colored dice block"
def colored_dice_block(block_rgb, dice_gray):
    # block_rgb: (size, size, 3)
    # dice_gray: (size, size), normalized 0-1
    # Multiply dice grayscale mask with block's average color
    avg_color = block_rgb.mean(axis=(0,1))  # RGB average
    # Scale dice mask by color
    colored_block = np.zeros_like(block_rgb)
    for c in range(3):
        colored_block[:,:,c] = dice_gray * avg_color[c]
    return colored_block.astype(np.uint8)

# Process each block
for y in range(0, height, size):
    for x in range(0, width, size):
        block = img_array[y:y+size, x:x+size]  # RGB block
        # Find dice that best matches luminance
        block_gray = block.mean(axis=2)  # average to grayscale
        j = min(dice_arrays, key=lambda k: np.mean((block_gray - dice_arrays[k]*255.0)**2))
        output_array[y:y+size, x:x+size] = colored_dice_block(block, dice_arrays[j])

# Convert back to image
result = Image.fromarray(output_array)
result.show()
result.save("output_colored.jpg")
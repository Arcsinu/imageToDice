from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = None
size = 7
path = r"C:\Users\Amine Khalil\Documents\Python\image to dice\input\enhanced.jpg"

image = Image.open(path).convert("L")
threshold = 128
bw_image = image.point(lambda x: 255 if x > threshold else 0, mode='L')

# Resize to multiple of size
width, height = bw_image.size
width -= width % size
height -= height % size
image = bw_image.resize((width, height))

# Load dice images and resize
dice = {i: Image.open(f"dice_{i}.png").convert("L").resize((size, size)) for i in range(7)}
dice_arrays = {i: np.array(dice[i]) for i in range(7)}

# Convert input to array
img_array = np.array(image)

# Replace each block
for y in range(0, height, size):
    for x in range(0, width, size):
        block = img_array[y:y+size, x:x+size]
        j = min(dice_arrays, key=lambda k: np.mean((block - dice_arrays[k])**2))
        img_array[y:y+size, x:x+size] = dice_arrays[j]

# Convert back to image
result = Image.fromarray(img_array)
result.show()
result.save("output_binary.jpg")
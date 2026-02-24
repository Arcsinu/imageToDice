import streamlit as st
from PIL import Image
import numpy as np
import io

# Allow very large images
Image.MAX_IMAGE_PIXELS = None
size = 14  # dice block size

# --- Load dice images ---
dice = {i: Image.open(f"dice_{i}.png").convert("L").resize((size, size)) for i in range(1,7)}
dice_arrays = {i: np.array(dice[i])/255.0 for i in range(1,7)}

# --- Functions ---
def colored_dice_block(block_rgb, dice_gray):
    avg_color = block_rgb.mean(axis=(0,1))
    colored_block = np.zeros_like(block_rgb)
    for c in range(3):
        colored_block[:,:,c] = dice_gray * avg_color[c]
    return colored_block.astype(np.uint8)

def process_image(image: Image.Image):
    # Resize image to multiple of size
    width, height = image.size
    width -= width % size
    height -= height % size
    image = image.resize((width, height))
    
    img_array = np.array(image)
    output_array = np.zeros_like(img_array)

    for y in range(0, height, size):
        for x in range(0, width, size):
            block = img_array[y:y+size, x:x+size]
            block_gray = block.mean(axis=2)
            j = min(dice_arrays, key=lambda k: np.mean((block_gray - dice_arrays[k]*255.0)**2))
            output_array[y:y+size, x:x+size] = colored_dice_block(block, dice_arrays[j])

    return Image.fromarray(output_array)

# --- Streamlit UI ---
st.title("Dice Image Generator 🎲")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])

if uploaded_file:
    # Open uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Process
    with st.spinner("Generating dice image..."):
        result = process_image(image)
    
    st.image(result, caption="Dice Image Output", use_column_width=True)

    # Download button
    buf = io.BytesIO()
    result.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    st.download_button("Download Image", data=byte_im, file_name="output_colored.jpg", mime="image/jpeg")
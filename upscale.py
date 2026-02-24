from PIL import Image

path = r"C:\Users\Amine Khalil\Documents\Python\image to dice\input\enhanced.jpg"
image = Image.open(path)

# Scale factor
scale = 2  # 2× larger
width, height = image.size

# Resize with high-quality resampling
image_highres = image.resize((width*scale, height*scale), Image.LANCZOS)

image_highres.show()
image_highres.save("enhanced.jpg")
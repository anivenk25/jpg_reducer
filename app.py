import streamlit as st
from PIL import Image
import io

def resize_image_to_target_size(image, target_kb, max_iter=20, initial_quality=95):
    target_bytes = target_kb * 1024

    # Set bounds for binary search
    low = 1
    high = 100
    best_quality = initial_quality
    best_data = None

    for i in range(max_iter):
        mid_quality = (low + high) // 2
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=mid_quality, optimize=True)
        size = buffer.tell()

        if size <= target_bytes:
            best_quality = mid_quality
            best_data = buffer.getvalue()
            low = mid_quality + 1
        else:
            high = mid_quality - 1

    return best_data, best_quality if best_data else (None, None)

# Streamlit UI
st.title("📦 Image Compressor to Target Size")
st.write("Upload an image and specify a target size (in KB). This app will compress the image accordingly.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
target_kb = st.number_input("Target size (KB)", min_value=10, max_value=2048, value=200, step=10)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original Image", use_column_width=True)

    if st.button("Compress Image"):
        data, quality = resize_image_to_target_size(img, target_kb)
        if data:
            st.success(f"Compression successful at quality={quality}")
            st.download_button(
                label="Download Compressed Image",
                data=data,
                file_name="compressed.jpg",
                mime="image/jpeg"
            )
        else:
            st.error("Could not compress to target size.")


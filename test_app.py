import streamlit as st
from PIL import Image
import os

# Import the required modules
try:
    from background_removal import remove_background
    from object_detection import detect_objects, remove_detected_objects
    from utils import save_image, draw_bounding_boxes
except ModuleNotFoundError as e:
    st.error(f"Missing module: {e}. Please ensure all dependencies are installed.")
    st.stop()

# Paths for saving files
OUTPUT_DIR = "data/output/"

# Application Title
st.title("Image Background and Object Processor")
st.sidebar.header("Options")

# Upload an image
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Select feature
options = st.sidebar.radio(
    "Select a Feature",
    ["Remove Background", "Replace Background", "Detect and Remove Objects"],
)

# Optional: Upload replacement background
replace_background = st.sidebar.file_uploader("Upload a background image (optional)", type=["jpg", "jpeg", "png"])
background_color = st.sidebar.color_picker("Or choose a background color", "#ffffff")

if uploaded_file:
    # Load the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    try:
        if options == "Remove Background":
            processed_image = remove_background(image)
            st.subheader("Background Removed")
            st.image(processed_image, use_column_width=True)

        elif options == "Replace Background":
            foreground = remove_background(image).convert("RGBA")
            if replace_background:
                background = Image.open(replace_background).resize(foreground.size).convert("RGBA")
            else:
                background = Image.new("RGBA", foreground.size, background_color)
            combined_image = Image.alpha_composite(background, foreground)
            st.subheader("Background Replaced")
            st.image(combined_image, use_column_width=True)

        elif options == "Detect and Remove Objects":
            from object_detection import detect_objects, remove_detected_objects
            detections = detect_objects(image)
            processed_image = remove_detected_objects(image, detections)
            st.subheader("Objects Removed")
            st.image(processed_image, use_column_width=True)

        # Save and download processed image
        output_path = os.path.join(OUTPUT_DIR, "processed_image.png")
        processed_image.save(output_path)
        with open(output_path, "rb") as file:
            btn = st.download_button(
                label="Download Processed Image",
                data=file,
                file_name="processed_image.png",
                mime="image/png",
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to get started.")

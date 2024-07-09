import streamlit as st
from PIL import Image, ImageDraw
import os
import io
import docx2txt  # Required for reading Word documents
from PyPDF2 import PdfReader  # Import PdfReader from PyPDF2

# Function to process the text content and generate image
def text_to_image(content, horizontal_size, vertical_size, start_with_gap=True):
    BG = Image.open("myfont/bg.png").convert("RGBA")
    sheet_width, sheet_height = BG.size
    draw = ImageDraw.Draw(BG)
    
    if start_with_gap:
        gap, ht = 100, 200  # Initial position with larger padding
    else:
        gap, ht = 0, 0  # Start from absolute top-left
    
    words = content.split()
    line_gap = gap
    
    for word in words:
        # Draw the word on the background image
        draw.text((line_gap, ht), word, fill="black")
        
        # Update gap for the next word
        line_gap += horizontal_size + 10  # Add spacing between words
    
    # Debugging: Display background image to check drawing
    st.image(BG, caption='Background Image', use_column_width=True)
    
    return BG

# Function to read text from a Word document
def read_docx(file):
    text = docx2txt.process(file)
    return text

# Function to read text from a PDF document
def read_pdf(uploaded_file):
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    text = ""
    with open("temp.pdf", "rb") as f:
        reader = PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    
    # Remove temporary file after reading
    os.remove("temp.pdf")
    
    return text

# Streamlit UI
st.set_page_config(page_title="Text2Hand", page_icon="📝")

st.markdown(
    """
    <style>
    .main {
        background-color: #2e2e2e;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
    }
    .stButton button {
        background-color: #333333;
        color: white;
        padding: 10px 24px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #555555;
    }
    .stFileUploader label, .stTextArea label {
        color: white;
    }
    .sidebar-content {
        background-color: #2e2e2e;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the sidebar layout for filters and file upload
with st.sidebar:
    st.title("Filters")
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload A File (Txt, Docx, Pdf)")
    text_input = st.text_area("Enter Text Here")
    horizontal_size = st.slider("Horizontal Size (Text)", min_value=20, max_value=100, value=40, step=2)
    vertical_size = st.slider("Vertical Size (Text)", min_value=20, max_value=200, value=100, step=2)
    start_with_gap = st.checkbox("Start with Gap (Top and Left)", value=True)

# Main content area
st.title("📝 Text2Hand")
st.markdown("Text2Hand is your digital scribe! Whether you're a student looking to spice up assignments or someone who enjoys the charm of handwritten notes, Text2Hand converts typed text into beautiful handwritten images effortlessly. Say goodbye to tedious writing and hello to handwritten text—all at your fingertips.")
st.markdown("Note: This app does not automatically recognize when to start a new line. Please ensure that your input text or files do not exceed the horizontal limit to maintain proper formatting.")
if st.button("Generate Handwritten Text"):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode('utf-8')
        elif uploaded_file.type == "application/pdf":
            content = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = read_docx(uploaded_file)
        
        st.write("Content:", content)  # Debugging: Output content to check
        
        image = text_to_image(content, horizontal_size, vertical_size, start_with_gap)
        st.image(image, caption='Generated Image', use_column_width=True)
        
        # Save image to a buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        st.download_button(
            label="Download Image",
            data=buffer,
            file_name="handwritten_image.png",
            mime="image/png"
        )

    elif text_input:
        image = text_to_image(text_input, horizontal_size, vertical_size, start_with_gap)
        st.image(image, caption='Generated Image', use_column_width=True)
        
        # Save image to a buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        st.download_button(
            label="Download Image",
            data=buffer,
            file_name="handwritten_image.png",
            mime="image/png"
        )

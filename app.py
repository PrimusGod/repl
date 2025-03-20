import streamlit as st
import requests
from PIL import Image
import io
from bs4 import BeautifulSoup
import base64
import time

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def search_google_images(image_base64):
    """Perform a Google Images reverse search"""
    try:
        search_url = "https://lens.google.com/uploadbyimage"
        results = {
            "title": "Google Lens",
            "url": search_url,
            "status": "Ready to search",
            "message": "Click to open Google Lens in a new tab"
        }
    except Exception as e:
        results = {
            "title": "Google Lens",
            "status": "Error",
            "message": str(e)
        }
    return results

def search_tineye(image_base64):
    """Perform a TinEye reverse search"""
    try:
        search_url = "https://tineye.com"
        results = {
            "title": "TinEye",
            "url": search_url,
            "status": "Ready to search",
            "message": "Click to open TinEye in a new tab"
        }
    except Exception as e:
        results = {
            "title": "TinEye",
            "status": "Error",
            "message": str(e)
        }
    return results

def search_bing_images(image_base64):
    """Perform a Bing Images reverse search"""
    try:
        search_url = "https://www.bing.com/images/search"
        results = {
            "title": "Bing Images",
            "url": search_url,
            "status": "Ready to search",
            "message": "Click to open Bing Images in a new tab"
        }
    except Exception as e:
        results = {
            "title": "Bing Images",
            "status": "Error",
            "message": str(e)
        }
    return results

def main():
    st.set_page_config(
        page_title="Multi-Engine Reverse Image Search",
        page_icon="🔍",
        layout="wide"
    )

    st.title("Multi-Engine Reverse Image Search")
    st.write("Upload an image to search across multiple reverse image search engines")

    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col2:
            st.write("Image Details:")
            st.write(f"Format: {image.format}")
            st.write(f"Size: {image.size}")
            st.write(f"Mode: {image.mode}")

        # Convert image to base64
        image_base64 = encode_image_to_base64(image)

        # Create tabs for different search engines
        tab1, tab2, tab3 = st.tabs(["Google Lens", "TinEye", "Bing Images"])

        # Perform searches
        with st.spinner('Preparing search results...'):
            google_results = search_google_images(image_base64)
            tineye_results = search_tineye(image_base64)
            bing_results = search_bing_images(image_base64)

        # Display results in tabs
        with tab1:
            st.subheader(google_results["title"])
            st.write(google_results["message"])
            if "url" in google_results:
                st.link_button("Open in Google Lens", google_results["url"])

        with tab2:
            st.subheader(tineye_results["title"])
            st.write(tineye_results["message"])
            if "url" in tineye_results:
                st.link_button("Open in TinEye", tineye_results["url"])

        with tab3:
            st.subheader(bing_results["title"])
            st.write(bing_results["message"])
            if "url" in bing_results:
                st.link_button("Open in Bing Images", bing_results["url"])

        st.info("Note: Due to search engine restrictions, results will open in new tabs on their respective websites.")

if __name__ == "__main__":
    main()

import streamlit as st
from PIL import Image
import math

st.set_page_config(layout="centered")
st.title("Aplikasi Konversi Citra: Grayscale, Biner, Terindeks")

uploaded_file = st.file_uploader("Unggah gambar")

mode = st.selectbox("Pilih jenis konversi", ["Grayscale", "Biner", "Terindeks"])

palette = {
    0: (0, 0, 0),       # Hitam
    1: (255, 0, 0),     # Merah
    2: (0, 255, 0),     # Hijau
    3: (0, 0, 255)      # Biru
}

def convert_to_grayscale(pixel):
    r, g, b = pixel
    return int(0.299 * r + 0.587 * g + 0.114 * b)

def convert_to_binary(gray_value, threshold=128):
    return 1 if gray_value >= threshold else 0

def find_closest_color_index(pixel):
    r1, g1, b1 = pixel
    closest_index = min(palette, key=lambda idx: math.sqrt(
        (r1 - palette[idx][0])**2 +
        (g1 - palette[idx][1])**2 +
        (b1 - palette[idx][2])**2
    ))
    return closest_index

def display_image(image, caption):
    with st.container():
        st.image(image, caption=caption, use_column_width=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    width, height = image.size

    # Menampilkan gambar asli di atas
    display_image(image, "Gambar Asli")

    # Konversi dan tampilkan hasil
    if mode == "Grayscale":
        gray_img = Image.new("L", (width, height))
        for y in range(height):
            for x in range(width):
                gray = convert_to_grayscale(image.getpixel((x, y)))
                gray_img.putpixel((x, y), gray)
        display_image(gray_img, "Gambar Grayscale")

    elif mode == "Biner":
        threshold = st.slider("Threshold (Ambang Batas)", 0, 255, 128)
        binary_img = Image.new("1", (width, height))
        for y in range(height):
            for x in range(width):
                gray = convert_to_grayscale(image.getpixel((x, y)))
                binary = convert_to_binary(gray, threshold)
                binary_img.putpixel((x, y), binary)
        display_image(binary_img, "Gambar Biner")

    elif mode == "Terindeks":
        indexed_img = Image.new("RGB", (width, height))
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                index = find_closest_color_index(pixel)
                indexed_img.putpixel((x, y), palette[index])
        display_image(indexed_img, "Gambar Terindeks")

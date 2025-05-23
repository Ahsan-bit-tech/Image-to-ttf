import cv2
import os
from openai_service import analyze_and_rename_images
from PIL import Image, ImageEnhance

def convert_to_black_and_white(image_path, output_path, contrast_factor=2):
    
    image = Image.open(image_path)
    bw_image = image.convert("L")
    enhancer = ImageEnhance.Contrast(bw_image)
    bw_image = enhancer.enhance(contrast_factor)
    bw_image.save(output_path)
    
    
def preprocess_image(image_path):
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, img, binary_img

def extract_and_save_characters(image_path, output_dir="extracted_characters"):
    modified_image = "images/modified_image.jpg"
    convert_to_black_and_white(image_path,modified_image,contrast_factor=3)
    contours, img, binary_img = preprocess_image(modified_image)
    os.makedirs(output_dir, exist_ok=True)
    char_images = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > 10 and h > 10:
            char_img = img[y:y+h, x:x+w]
            char_img = cv2.resize(char_img, (64, 64), interpolation=cv2.INTER_AREA)
            char_images.append((char_img, f"char_{i+1}.png"))
        
    for char_img, filename in char_images:
        file_path = os.path.join(output_dir, filename)
        cv2.imwrite(file_path, char_img)
    
    print(f"Saved {len(char_images)} characters to '{output_dir}'.")
    analyze_and_rename_images()

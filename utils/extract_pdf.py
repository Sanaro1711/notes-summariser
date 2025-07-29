#-------------------------------------------------------------------------------
# Name:        extract_pdf.py
# Purpose:     Extract text from pdfs given by user
#
# Author:      Sanidhya Arora
#
# Created:     21/07/2025
# Copyright:   (c) sanid 2025
#-------------------------------------------------------------------------------
from pypdf import PdfReader
import fitz
from PIL import Image
from gemini_class import Gemini
import os
from dotenv import load_dotenv
import sys

load_dotenv()
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

def extract_text_and_images_from_pdf(filepath):
    """Takes filepath, opens that file, and extracts text from it"""

    try:
        image_paths = []
        pdf_file = fitz.open(filepath)
        numPages = len(pdf_file)
        all_text = ''

        # iterate through all the pages, and store the text in variable
        for i in range(numPages):
            page = pdf_file.load_page(i)

            # get the text
            text = page.get_text()
            all_text += text

            # get the images
            image_list = page.get_images(full=True)
            img_num = 1
            for img in (image_list):
                # get the XREF of the image
                xref = img[0]

                # extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]

                # get the image extension
                image_ext = base_image["ext"]

                # save the image
                output_filename = f"image{img_num}_{i}.{image_ext}"
                output_path = os.path.join(UPLOAD_FOLDER, "images", output_filename)

                img_num+=1
                image_paths.append(output_path)
                with open(output_path, "wb") as image_file:
                    image_file.write(image_bytes)

                    #print(f"[+] Image saved as image_{i}.{image_ext}")


        # remove any extra lines in text - clean up data
        lines = all_text.splitlines()
        text = cleanup_data(lines)

        return text, image_paths

    except Exception as e:
        print(f"error: {e}")
        return "", []


def extract_image_bytes(image_paths):
    """take list of images and return the bytes of each in a list form"""
    image_bytes = []

    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            image_byte = f.read()
            image_bytes.append(image_byte)

    return image_bytes

def cleanup_data(lines):
    """cleans the data by removing extra newlines"""
    double = True
    write = 0

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        if lines[i] == '' and not double:
            lines[write] = lines[i]
            write+=1
            double = True

        elif lines[i] != '':
            lines[write] = lines[i]
            write+=1
            double = False


    lines = lines[:write]
    text = "\n".join(lines)

    return text


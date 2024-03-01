from PIL import Image
from io import BytesIO
import base64
from IPython.display import display, HTML
import pandas as pd
import pdfkit
import time
import sys

def resize_image(image, max_width):
    width_percent = (max_width / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percent)))
    return image.resize((max_width, new_height), Image.LANCZOS)


def replace_words_with_resized_images(text, max_image_width):
    word_image_mapping = {
        'safety': './safety.jpg',
        'caution': './caution.jpg',
        'warning': './warning.jpg'
        # Add more mappings as needed
    }

    for word, image_path in word_image_mapping.items():
        image = Image.open(image_path)

        # Resize the image
        resized_image = resize_image(image, max_image_width)

        # Convert image to base64 encoding
        image_buffer = BytesIO()
        image.save(image_buffer, format="PNG")
        image_base64 = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

        # Replace the word with an HTML <img> tag
        text = text.replace(word, f'<img src="data:image/png;base64,{image_base64}" alt="{word}" style="vertical-align: middle;  max-width: {max_image_width}px;">')

    return text

def process_and_save_to_table(sentences, max_image_width):
    data = {'Modified Sentence': []}

    for sentence in sentences:
        modified_text = replace_words_with_resized_images(sentence, max_image_width)
        data['Modified Sentence'].append(modified_text)

    df = pd.DataFrame(data)
    display(HTML(df.to_html('result.html',escape=False, header=False, index=False)))  # Display the table

def html_to_pdf(html_path, pdf_path):
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
    }
    
    wkhtmltopdf_path = r'.\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        
    pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)

# Example usage
user_input = '''This is a safety message. Exercise caution to avoid warning.
Another sentence with caution. Be aware of the danger.
A warning about safety. Stay cautious and avoid risks.
I have received a warning call with no safety.'''
#user_input = sys.stdin.read()
sentences=user_input.split('\n')

max_image_width = 20
process_and_save_to_table(sentences, max_image_width)
#time.sleep(5)
html_path = 'result.html'
pdf_path = 'result.pdf'

html_to_pdf(html_path, pdf_path)
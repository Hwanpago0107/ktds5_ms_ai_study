from dotenv import load_dotenv
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis.models import VisualFeatures
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import openai

load_dotenv()

# Set your API key and Azure settings
aiservice_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
aiservice_api_key = os.getenv("AI_SERVICE_API_KEY")

# print("aiservice_endpoint:", aiservice_endpoint)
# print("aiservice_api_key:", aiservice_api_key)

credential = AzureKeyCredential(aiservice_api_key)

# Initialize the Azure Image Analysis client
client = ImageAnalysisClient(
    endpoint=aiservice_endpoint,
    credential=credential
)

def get_image_info():
    file_path = input("Enter the path to the image file: ")
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.TAGS
                         ,VisualFeatures.CAPTION
                         ,VisualFeatures.OBJECTS
                        ],
                        model_version="latest"
    )

    if result.tags is not None:
        print("Image Tags:")
        for tag in result.tags.list:
            print(f" - {tag.name} (confidence: {tag.confidence:.4f})")
    if result.caption is not None:
        print("Image Caption:")
        print(f" - {result.caption.text} (confidence: {result.caption.confidence:.4f})")
    if result.objects is not None:
        print("Image Objects:")
        bounding_boxes = []
        for obj in result.objects.list:
            print(f" - {obj.tags[0].name} = {obj.bounding_box} (confidence: {obj.tags[0].confidence:.4f})")
            bounding_boxes.append(obj)

    draw_bounding_boxes(file_path, bounding_boxes)

def draw_bounding_boxes(image_path, bounding_boxes):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for box in bounding_boxes:
        x = box.bounding_box.x
        y = box.bounding_box.y
        w = box.bounding_box.width
        h = box.bounding_box.height
        draw.rectangle(
            ((x,y),(x + w, y + h)),
            outline="red", 
            width=5
        )
        draw.text((x, y), box.tags[0].name, fill="red")

    image.show()

if __name__ == "__main__":
    get_image_info()
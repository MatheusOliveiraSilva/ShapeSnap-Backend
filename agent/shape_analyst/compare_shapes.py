import base64
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agent.shape_analyst.prompts import SHAPE_ANALYST_PROMPT
from agent.shape_analyst.models import Feedback
from pathlib import Path
from dotenv import load_dotenv

root = Path(__file__).resolve().parent.parent.parent

load_dotenv(dotenv_path=root / '.env')

def encode_image_to_base64(image_path):
    """
    Encode an image to base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_images(before_image_path, after_image_path, prompt=SHAPE_ANALYST_PROMPT):
    """
    Send before and after images to a vision model and get a structured analysis
    """
    # Initialize the vision model
    vision_model = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o",
        max_tokens=2000
    )
    
    vision_model_with_structured_output = vision_model.with_structured_output(Feedback)

    # Encode the images
    before_base64_image = encode_image_to_base64(before_image_path)
    after_base64_image = encode_image_to_base64(after_image_path)
    
    # Create the message with both images
    message = [
        SystemMessage(content="You are a shape analyst that compares before and after images to provide detailed body composition feedback."),
        HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "text", "text": "BEFORE image:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{before_base64_image}",
                        "detail": "high"
                    }
                },
                {"type": "text", "text": "AFTER image:"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{after_base64_image}",
                        "detail": "high"
                    }
                }
            ]
        )
    ]
    
    # Get the response
    response = vision_model_with_structured_output.invoke(message)
    return response

if __name__ == "__main__":
    before_image_path = root / "agent/shape_analyst/images/before1.png"
    after_image_path = root / "agent/shape_analyst/images/after1.png"
    analysis = analyze_images(before_image_path, after_image_path)
    print(analysis)
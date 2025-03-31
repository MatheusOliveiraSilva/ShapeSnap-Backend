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

class ShapeAnalyst:
    def __init__(self, api_key=None):
        """
        Initialize the ShapeAnalyst with OpenAI API key
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.vision_model = ChatOpenAI(
            api_key=self.api_key,
            model="gpt-4o",
            temperature=0,
            max_tokens=2000
        )
        self.vision_model_with_structured_output = self.vision_model.with_structured_output(Feedback)

    @staticmethod
    def encode_image_to_base64(image_path):
        """
        Encode an image to base64 string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_images(self, before_image_path, after_image_path, prompt=SHAPE_ANALYST_PROMPT, language="English"):
        """
        Send before and after images to a vision model and get a structured analysis
        
        Args:
            before_image_path (str or Path): Path to the before image
            after_image_path (str or Path): Path to the after image
            prompt (str): The prompt template to use for analysis
            language (str): The language for the analysis output
            
        Returns:
            Feedback: Structured feedback about the body composition changes
        """
        # Encode the images
        before_base64_image = self.encode_image_to_base64(before_image_path)
        after_base64_image = self.encode_image_to_base64(after_image_path)
        
        # Create the message with both images
        message = [
            SystemMessage(content="You are a shape analyst that compares before and after images to provide detailed body composition feedback."),
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt.format(language=language)},
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
        response = self.vision_model_with_structured_output.invoke(message)
        return response

if __name__ == "__main__":
    # Create an instance of ShapeAnalyst
    analyst = ShapeAnalyst()
    
    # Define the image paths
    before_image_path = root / "agent/shape_analyst/images/before1.png"
    after_image_path = root / "agent/shape_analyst/images/after1.png"
    
    # Perform the analysis
    analysis = analyst.analyze_images(before_image_path, after_image_path, language="Portuguese")
    print(analysis)
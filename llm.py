import google.generativeai as genai
from PIL import Image
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Define the Model class
class Model:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
    def get_response(self, prompt, image=None):
        if image:
            img = Image.open(image)
            response = self.model.generate_content([prompt, img]) 
        else:
            response = self.model.generate_content([prompt]) 
        return response.text
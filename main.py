import cv2
import pytesseract # type: ignore
from google import genai
import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled
from llm_setup import model  

set_tracing_disabled(True)


def preprocess_image(image):
    try:
        img = cv2.imread(image)
        if img is None:
            raise FileNotFoundError(f"Image not found: {image}")
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('gray_image.jpg', gray)
        # Apply thresholding
        _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite('thresholded_image.jpg', threshold)
        return threshold
    except Exception as e:
        print(f"Error in preprocess_image: {e}")
        raise

def extract_text(image):
    try:
        text = pytesseract.image_to_string(image)
        if not text.strip():
            print("Warning: No text extracted from image.")
        return text
    except pytesseract.TesseractNotFoundError:
        print("Tesseract is not installed or not in PATH.")
        raise
    except Exception as e:
        print(f"Error in extract_text: {e}")
        raise

async def ai_extract(text_content):
    try:
        agent = Agent(
            name="receipt_parser",
            instructions="""
            You are a receipt parser AI. I will provide you with text extracted from an image of a store receipt.

            Return a JSON object with the following structure:
            {
            "total": <float>,
            "business": "<string>",
            "items": [{"title": "<string>", "quantity": <int>, "price": <float>}],
            "transaction_timestamp": "<ISO8601 timestamp>"
            }

            Prices are in USD and should be returned as floating point numbers in dollar format (e.g., 4.99). 
            Do not return any text or explanation — only the JSON object.
            """,
            model=model
        )
        response = await Runner.run(agent, text_content)
        full_text = response.final_output
        if full_text is None:
            raise ValueError("No response text received from Gemini API.")
        json_start = full_text.find('{')
        json_end = full_text.rfind('}') + 1
        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON object found in the response.")
        return full_text[json_start:json_end]
    except Exception as e:
        print(f"Error in ai_extract: {e}")
        raise

if __name__ == '__main__':
    try:
        image_path = r"raw_receipts\receipt2.png"
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file does not exist: {image_path}")

        preprocessed_image = preprocess_image(image_path)
        text_content = extract_text(preprocessed_image)
        print("Extracted Text Content:")
        print(text_content)

        import asyncio
        json_data = asyncio.run(ai_extract(text_content))

        os.makedirs('json_receipt', exist_ok=True)
        with open(r'json_receipt/receipt.json', 'w') as f:
            f.write(json_data)
        print("JSON data written to json_receipt/receipt.json")
    except Exception as e:
        print(f"Fatal error: {e}")
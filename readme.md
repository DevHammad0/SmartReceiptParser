# Receiptly

Receiptly extracts text from an image of a store receipt and converts it into a structured JSON object using OCR (Tesseract), OpenCV, and Gemini AI.

## Requirements

- Python 3.x
- OpenCV
- pytesseract
- openai-agents
- **Tesseract-OCR** (must be installed separately and added to your system PATH)

## Installation

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install Tesseract-OCR (separately):**
    - Download and install from [Tesseract at UB Mannheim](https://github.com/tesseract-ocr/tesseract).
    - Add the Tesseract install directory (e.g., `C:\Program Files\Tesseract-OCR`) to your system PATH.
    - Test installation with:
      ```sh
      tesseract --version
      ```

4. **Set up your Gemini API key:**
    - Create a `.env` file in the project root:
      ```
      GEMINI_API_KEY=your_gemini_api_key_here
      ```

## Usage

1. **Add a receipt image**  
   Place your receipt image (e.g., `receipt2.png`) in the `raw_receipts` folder.

2. **Run the script:**
    ```sh
    python main.py
    ```

3. **Output:**  
   - The extracted text will be printed to the console.
   - The structured JSON will be saved to `json_receipt/receipt.json` (full path will be shown after running).

## Project Structure

- `main.py`: Main script for image processing, OCR, and AI extraction.
- `llm_setup.py`: Gemini AI model setup and configuration.
- `raw_receipts/`: Place your input receipt images here.
- `json_receipt/`: Output folder for generated JSON files.
- `requirements.txt`: Python dependencies.
- `readme.md`: Project documentation.

## Troubleshooting

- **Tesseract not found:**  
  Ensure Tesseract-OCR is installed and its path is added to your system PATH. Test with `tesseract --version` in your terminal.
- **No internet connection:**  
  Gemini AI requires an active internet connection.
- **API key errors:**  
  Make sure your `.env` file is present and contains a valid `GEMINI_API_KEY`.


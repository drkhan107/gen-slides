# GenSlides

GenSlides is a web application that generates PowerPoint slides from text content or PDF files. It is built using Streamlit and provides an easy-to-use interface for creating presentations quickly.

## Features

- Generate PowerPoint slides from text content or PDF files.
- Customize the agenda and content type (text or PDF).
- Advanced options for setting the maximum number of pages and specifying page ranges.
- Download the generated slides directly from the application.
- By default, supports up to 20 pages (approximately 45,000 characters). Text length beyond this limit will be truncated.
- Currently supports Gemini models only (Gemini 1.5 Flash by default).

## Installation

To install and run the application locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/genslides.git
    cd genslides
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set the environment variable `GOOGLE_API_KEY` with your API key:
    ```bash
    export GOOGLE_API_KEY=your_google_api_key
    ```
    On Windows:
    ```bash
    set GOOGLE_API_KEY=your_google_api_key
    ```

5. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Open the application in your web browser (usually at `http://localhost:8501`).
2. Enter the agenda for your presentation.
3. Choose the content type (Text or PDF).
    - If you choose Text, enter the text content.
    - If you choose PDF, upload a PDF file.
4. (Optional) Set advanced options such as the maximum number of pages and page range.
5. Click on the "Generate Slides" button to create the PowerPoint slides.
6. Once the slides are generated, download the file using the provided download button.


## Credits
This project was developed by [Asif Iqbal Khan](https://github.com/drkhan107). Feel free to customize the content as needed with appropriate attribution to the original author. 

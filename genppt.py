import json
import os
from typing import Optional, List, Dict, Any

from ppt import SlideDeck
from gemini import GeminiModel, LangchainGemini
from prompts import get_ppt_prompt
from utils import parse_page_ranges

# Define available models
MODELS: Dict[str, Any] = {
    "gemini_flash_l": LangchainGemini,
    "gemini_flash": GeminiModel
}

class GenPPT:
    """
    A class to generate PowerPoint presentations from text or PDF sources using AI models.
    """

    def __init__(
        self,
        source: str = "",
        text: str = "",
        agenda: str = "Generic",
        model_name: str = "gemini_flash_l",
        llm_api_key: Optional[str] = None,
        pages: Optional[str] = None,
        max_pages: int = 20,
    ):
        """
        Initialize the GenPPT object.

        Args:
            source (str): Path to the source PDF file.
            text (str): Input text for presentation generation.
            agenda (str): Agenda type for the presentation.
            model_name (str): Name of the AI model to use.
            llm_api_key (Optional[str]): API key for the language model.
            pages (Optional[str]): Page range to extract from PDF.
            max_pages (int): Maximum number of pages to process.
        """
        self.source: Optional[str] = source.strip() or None
        self.text: Optional[str] = text.strip() or None
        self.agenda: str = agenda.strip() or "Generic"

        self.max_pages: int = max_pages
        self.pages=pages

        self.model_name: str = model_name.strip()
        try:
            self.llm = MODELS[self.model_name](API_KEY=llm_api_key)
        except KeyError:
            print(f"Warning: Model '{self.model_name}' not found. Using default model.")
            self.llm = MODELS["gemini_flash_l"](API_KEY=llm_api_key)

    def run(self) -> Optional[Any]:
        """
        Run the presentation generation process.

        Returns:
            Optional[Any]: Generated presentation or None if an error occurs.
        """
        try:
            if self.text is None:
                if self.source is not None:
                    self.text = self.extract_markdown_from_pdf()
                else:
                    raise ValueError("Both source and text cannot be None.")

            slides = self.generate_slides()
            return self.generate_presentation(slides)
        except Exception as e:
            print(f"An error occurred during presentation generation: {e}")
            return None

    def extract_markdown_from_pdf(self) -> str:
        """
        Extract markdown content from the source PDF.

        Returns:
            str: Extracted markdown text.

        Raises:
            ImportError: If pymupdf4llm is not installed.
            FileNotFoundError: If the source PDF file is not found.
        """
        try:
            import pymupdf4llm
        except ImportError:
            raise ImportError("pymupdf4llm is required for PDF extraction. Please install it.")

        if not os.path.exists(self.source):
            raise FileNotFoundError(f"Source PDF file not found: {self.source}")

        print(f"Extracting {len(self.pages)} pages")
        return pymupdf4llm.to_markdown(self.source, pages=self.pages)

    def generate_slides(self) -> List[Dict[str, Any]]:
        """
        Generate slide content using the AI model.

        Returns:
            List[Dict[str, Any]]: List of slide data dictionaries.

        Raises:
            ValueError: If the model response is invalid.
        """
        prompt = f"{get_ppt_prompt()}\nAgenda: {self.agenda}\nContent: {self.text}"
        resp = self.llm.execute(prompt)

        try:
            return json.loads(resp.content.strip("```").replace("json", "").strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid model response: {e}")

    def generate_presentation(self, content: List[Dict[str, Any]]) -> Any:
        """
        Create the final presentation using the generated slide content.

        Args:
            content (List[Dict[str, Any]]): List of slide data dictionaries.

        Returns:
            Any: The generated presentation object.
        """
        deck = SlideDeck()
        title_slide_data, *slides_data = content
        return deck.create_presentation(title_slide_data, slides_data)
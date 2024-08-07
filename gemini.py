import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI

generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        #candidate_count=1,
        #stop_sequences=['x'],
        max_output_tokens=4096,
        temperature=0.1
)
class GeminiModel:
    """
    This class is used to interact with the Google LLM models for text generation.

    Args:
        model: The name of the model to be used. Defaults to 'gemini-pro'.
        max_output_tokens: The maximum number of tokens to generate. Defaults to 1024.
        top_p: The probability of generating the next token. Defaults to 1.0.
        temperature: The temperature of the model. Defaults to 0.0.
        top_k: The number of top tokens to consider. Defaults to 5.
    """

    def __init__(self,
                 model_name: Optional[str] = 'gemini-1.5-flash',
                 ):
        
        
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_name) # type: ignore
        

    def execute(self, prompt: str) -> str:
        
        try:
            prompt_tokens = self.model.count_tokens(prompt).total_tokens
            print(f"Input tokens: {prompt_tokens}")
            response = self.model.generate_content(prompt, generation_config=generation_config)
            output_tokens = self.model.count_tokens(response.text).total_tokens
            print(f"Output tokens: {output_tokens}")

            return response.text,{'prompt_tokens':prompt_tokens,"total_tokens":output_tokens}
        except Exception as e:
            return f"An error occurred: {e}"
        

class LangchainGemini:
    """
    This class is used to interact with the Google LLM models using Langchain for text generation.

    Args:
        model: The name of the model to be used. Defaults to 'gemini-pro'.
        max_output_tokens: The maximum number of tokens to generate. Defaults to 1024.
        top_p: The probability of generating the next token. Defaults to 1.0.
        temperature: The temperature of the model. Defaults to 0.0.
        top_k: The number of top tokens to consider. Defaults to 5.
    """

    def __init__(self,
                 model_name: Optional[str] = 'gemini-1.5-flash',
                 API_KEY=None
                 ):
    
        #load_dotenv()
        self.model= ChatGoogleGenerativeAI(model=model_name,
                                            temperature=0.5,
                                            max_tokens=4096,
                                            timeout=None,
                                            max_retries=2,
                                            google_api_key=API_KEY)
        
    def execute(self, prompt: str) -> str:
        
        try:
            response = self.model.invoke(prompt)
            return response
        except Exception as e:
            return f"An error occurred: {e}"
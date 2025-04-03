import json
from typing import Any, Dict

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from backend.config import settings


class LicenseAnalyzer:
    """Class for analyzing software licenses using LLMs"""

    def __init__(self, model_name: str = settings.DEFAULT_MODEL):
        """Initialize the license analyzer with specified LLM model

        Args:
            model_name: The name of the LLM model to use
        """
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model_name=model_name, temperature=0, api_key=settings.OPENAI_API_KEY
        )

        # Create the prompt template for license analysis
        self.license_prompt = PromptTemplate(
            input_variables=["license_text"],
            template="""You are an expert in software licensing. Analyze the following license text and extract key information:

{license_text}

Provide the following information in a structured format:
1. License Type (e.g., MIT, GPL, Apache, etc.)
2. Permissions (what users are allowed to do)
3. Limitations (what users cannot do)
4. Obligations (what users must do)

Format your response as a JSON object with the following structure:
{{
  "license_type": "string",
  "permissions": ["string", "string", ...],
  "limitations": ["string", "string", ...],
  "obligations": ["string", "string", ...]
}}
""",
        )

        # Create the LLM chain
        self.license_chain = LLMChain(
            llm=self.llm, prompt=self.license_prompt, verbose=settings.DEBUG
        )

    def analyze_license(self, license_text: str) -> Dict[str, Any]:
        """Analyze a license text and extract structured information

        Args:
            license_text: The license text to analyze

        Returns:
            A dictionary containing the license type, permissions, limitations, and obligations
        """
        try:
            result = self.license_chain.invoke({"license_text": license_text})
            # Parse the JSON response
            try:
                return json.loads(result["text"])
            except json.JSONDecodeError:
                # If the response is not valid JSON, return a basic structure
                return {
                    "license_type": "Unknown",
                    "permissions": [],
                    "limitations": [],
                    "obligations": [],
                }
        except Exception as e:
            print(f"Error analyzing license: {e}")
            return {
                "license_type": "Unknown",
                "permissions": [],
                "limitations": [],
                "obligations": [],
            }

    def get_package_license(
        self, package_name: str, ecosystem: str = "python"
    ) -> Dict[str, Any]:
        """Get license information for a package

        Args:
            package_name: The name of the package
            ecosystem: The package ecosystem (python, npm, etc.)

        Returns:
            A dictionary containing the license information
        """
        # TODO: Implement fetching license information from package repositories
        # For now, return a placeholder
        return {
            "license_type": "Unknown",
            "permissions": [],
            "limitations": [],
            "obligations": [],
        }

import logging
import re

import colorama
import requests
import streamlit as st
from colorama import Fore, Style

# Initialize colorama for colored console output
colorama.init(autoreset=True)


# Configure logging with colored console output
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
            record.msg = f"{self.COLORS[levelname]}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

# Apply the colored formatter to the root logger
for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(
            ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

logger = logging.getLogger("licenSage-frontend")

# Set page configuration
st.set_page_config(
    page_title="LicenSage",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API endpoint (will need to be updated when deployed)
API_URL = "http://localhost:8000"


def main():
    # App title and description
    st.title("LicenSage 📝")
    st.subheader("GenAI-powered License Compliance Tool")

    st.markdown(
        """
    LicenSage helps you analyze software dependencies and identify license compliance issues.
    Enter a GitHub repository URL or upload a dependency file to get started.
    """
    )

    # Create a single input section with two options
    st.header("Analyze Dependencies")

    # Option selection
    input_method = st.radio(
        "Select input method:", ["GitHub Repository URL", "Upload Dependency File"]
    )

    if input_method == "GitHub Repository URL":
        # GitHub URL input
        github_url = st.text_input(
            "Enter GitHub Repository URL",
            placeholder="https://github.com/username/repo",
        )

        if st.button("Analyze Repository"):
            if github_url and is_valid_github_url(github_url):
                with st.spinner("Analyzing repository..."):
                    try:
                        logger.info(f"Analyzing GitHub repository: {github_url}")
                        response = requests.post(
                            f"{API_URL}/api/github/analyze",
                            json={"url": github_url},
                            timeout=30,
                        )
                        if response.status_code == 200:
                            logger.info(
                                f"Successfully analyzed GitHub repository: {github_url}"
                            )
                            display_results(response.json())
                        else:
                            error_msg = (
                                f"Error: {response.status_code} - {response.text}"
                            )
                            logger.error(error_msg)
                            st.error(error_msg)
                    except requests.RequestException as e:
                        error_msg = f"API request failed: {str(e)}"
                        logger.error(error_msg, exc_info=True)
                        st.error(error_msg)
            else:
                warning_msg = "Please enter a valid GitHub repository URL"
                logger.warning(warning_msg)
                st.warning(warning_msg)

    else:  # Upload Dependency File
        # File type detection will be handled by the backend
        uploaded_file = st.file_uploader(
            "Upload your dependency file", type=["txt", "json", "toml", "csproj", "xml"]
        )

        if st.button("Analyze File"):
            if uploaded_file is not None:
                with st.spinner("Analyzing dependencies..."):
                    try:
                        logger.info(f"Uploading dependency file: {uploaded_file.name}")

                        # Create a multipart form request with the file
                        files = {
                            "file": (uploaded_file.name, uploaded_file, "text/plain")
                        }

                        response = requests.post(
                            f"{API_URL}/api/dependency/upload", files=files, timeout=30
                        )

                        if response.status_code == 200:
                            logger.info(
                                f"Successfully analyzed dependency file: {uploaded_file.name}"
                            )
                            display_results(response.json())
                        else:
                            error_msg = (
                                f"Error: {response.status_code} - {response.text}"
                            )
                            logger.error(error_msg)
                            st.error(error_msg)
                    except Exception as e:
                        error_msg = f"Error processing file: {str(e)}"
                        logger.error(error_msg, exc_info=True)
                        st.error(error_msg)
            else:
                warning_msg = "Please upload a dependency file"
                logger.warning(warning_msg)
                st.warning(warning_msg)


def is_valid_github_url(url):
    """Check if the URL is a valid GitHub repository URL"""
    pattern = r"^https?://github\.com/[\w.-]+/[\w.-]+/?.*$"
    return bool(re.match(pattern, url))


def display_results(data):
    """Display license analysis results"""
    st.header("License Analysis Report")

    if not data.get("packages"):
        st.info("No packages found or no license information available.")
        return

    # Display resources used if available
    if data.get("resources_used"):
        st.subheader("Resources Used")
        for resource in data["resources_used"]:
            st.write(f"- {resource}")
        st.divider()

    # Display package information
    st.subheader("Package Licenses")
    for pkg in data["packages"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.subheader(pkg["package_name"])
            st.caption(f"License: {pkg.get('license_type', 'Unknown')}")

        with col2:
            if pkg.get("permissions"):
                st.write("✅ **Permissions:**")
                st.write(", ".join(pkg["permissions"]))

            if pkg.get("limitations"):
                st.write("⚠️ **Limitations:**")
                st.write(", ".join(pkg["limitations"]))

            if pkg.get("obligations"):
                st.write("📋 **Obligations:**")
                st.write(", ".join(pkg["obligations"]))

        st.divider()


if __name__ == "__main__":
    try:
        logger.info("Starting LicenSage frontend application")
        main()
    except Exception as e:
        logger.critical(f"Unhandled exception: {str(e)}", exc_info=True)
        st.error(f"An unexpected error occurred: {str(e)}")

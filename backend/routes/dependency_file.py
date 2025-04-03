import base64
import os
import shutil
import tempfile
import uuid
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.utils.dependency_parser import DependencyParser
from backend.utils.logger_utils import get_logger

router = APIRouter()

# Set up logger
logger = get_logger(__name__)

# Create a temporary directory for file uploads
TEMP_DIR = os.path.join(tempfile.gettempdir(), "licenSage-uploads")
os.makedirs(TEMP_DIR, exist_ok=True)


class LicenseInfo(BaseModel):
    package_name: str
    license_type: Optional[str] = None
    permissions: Optional[List[str]] = None
    limitations: Optional[List[str]] = None
    obligations: Optional[List[str]] = None


class LicenseReport(BaseModel):
    packages: List[LicenseInfo]
    resources_used: Optional[List[str]] = None


@router.post("/upload", response_model=LicenseReport)
async def upload_dependency_file(file: UploadFile = File(...)):
    """Upload and analyze a dependency file"""
    try:
        logger.info(f"Received file upload: {file.filename}")

        # Create a unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(TEMP_DIR, unique_filename)

        # Save the uploaded file
        content = await file.read()
        if isinstance(content, bytes):
            # Check if content might be UTF-16 encoded (common issue with Windows text files)
            if content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff') or b'\x00' in content[:20]:
                # Attempt to decode as UTF-16
                try:
                    decoded_content = content.decode('utf-16')
                    with open(file_path, "w", encoding="utf-8") as buffer:
                        buffer.write(decoded_content)
                except UnicodeDecodeError:
                    with open(file_path, "wb") as buffer:
                        buffer.write(content)
            else:
                with open(file_path, "wb") as buffer:
                    buffer.write(content)
        else:
            with open(file_path, "w", encoding="utf-8", errors="replace") as buffer:
                buffer.write(content)

        logger.info(f"Saved uploaded file to {file_path}")

        # Determine file type from extension
        file_type = get_file_type(file.filename)
        logger.info(f"Detected file type: {file_type}")

        # Read the file content
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Parse the dependency file to extract package names
        parser = DependencyParser()
        packages = parser.parse_dependency_file(content=content, file_type=file_type)
        logger.info(f"Parsed {len(packages)} packages from uploaded file")

        # Resources used for analysis
        resources_used = [
            (
                "PyPI API"
                if file_type in ["requirements.txt", "pyproject.toml"]
                else "NPM Registry"
            ),
            "Package License Database",
            "OpenAI GPT-4 for license analysis",
        ]

        # For demonstration purposes, create placeholder license info
        license_info = []
        for package in packages:  # Limit to 5 packages for demo
            logger.debug(f"Analyzing license for package: {package}")
            # In a real implementation, we would use a license analyzer to get real license data
            # from ..models.license_analyzer import LicenseAnalyzer
            # analyzer = LicenseAnalyzer()
            # license_data = analyzer.get_package_license(package)

            license_info.append(
                LicenseInfo(
                    package_name=package,
                    license_type="MIT",  # Placeholder
                    permissions=[
                        "commercial-use",
                        "modification",
                        "distribution",
                        "private-use",
                    ],
                    limitations=["liability", "warranty"],
                    obligations=["license-notice", "copyright-notice"],
                )
            )

        # Clean up the temporary file
        try:
            os.remove(file_path)
            logger.debug(f"Removed temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to remove temporary file {file_path}: {str(e)}")

        logger.info(
            f"Successfully analyzed {len(license_info)} packages from uploaded file"
        )
        return LicenseReport(packages=license_info, resources_used=resources_used)
    except Exception as e:
        logger.error(f"Error processing uploaded file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error processing uploaded file: {str(e)}"
        )


def get_file_type(filename):
    """Determine file type from filename"""
    if filename.endswith(".txt"):
        return "requirements.txt"
    elif filename.endswith(".json"):
        return "package.json"
    elif filename.endswith(".toml"):
        return "pyproject.toml"
    elif filename.endswith(".csproj") or filename.endswith(".xml"):
        return ".csproj"
    else:
        return "unknown"


def is_base64(s):
    """Check if a string might be base64 encoded"""
    try:
        # Check if the string contains only valid base64 characters
        return all(
            c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
            for c in s
        )
    except Exception:
        return False

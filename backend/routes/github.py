from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from backend.utils.logger_utils import get_logger

router = APIRouter()

# Set up logger
logger = get_logger(__name__)


class GithubRepo(BaseModel):
    url: HttpUrl


class LicenseInfo(BaseModel):
    package_name: str
    license_type: Optional[str] = None
    permissions: Optional[List[str]] = None
    limitations: Optional[List[str]] = None
    obligations: Optional[List[str]] = None


class LicenseReport(BaseModel):
    packages: List[LicenseInfo]
    resources_used: Optional[List[str]] = None


@router.post("/analyze", response_model=LicenseReport)
async def analyze_github_repo(repo: GithubRepo):
    """Analyze a GitHub repository for license information"""
    try:
        logger.info(f"Analyzing GitHub repository: {repo.url}")

        # Extract packages from GitHub repository
        # This is a placeholder - actual implementation would fetch packages from GitHub
        # In a real implementation, we would:
        # 1. Clone or download the GitHub repository
        # 2. Identify the package structure (is it a single package or contains multiple packages)
        # 3. Extract package information and dependencies

        # For demonstration purposes, we'll use sample data
        packages = ["numpy", "pandas", "requests"]
        logger.debug(f"Extracted packages: {packages}")

        # Analyze licenses for each package
        license_info = []
        resources_used = [
            "GitHub API",
            "Package License Database",
            "OpenAI GPT-4 for license analysis",
        ]

        # Initialize license analyzer when needed for actual analysis
        # from ..models.license_analyzer import LicenseAnalyzer
        # analyzer = LicenseAnalyzer()

        for package in packages:
            logger.debug(f"Analyzing license for package: {package}")
            # In a real implementation, we would use the analyzer to get real license data
            # license_data = analyzer.get_package_license(package)

            # Placeholder for license analysis
            license_info.append(
                LicenseInfo(
                    package_name=package,
                    license_type="MIT",
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

        logger.info(
            f"Successfully analyzed {len(license_info)} packages from GitHub repository: {repo.url}"
        )
        return LicenseReport(packages=license_info, resources_used=resources_used)
    except Exception as e:
        logger.error(f"Error analyzing GitHub repository: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

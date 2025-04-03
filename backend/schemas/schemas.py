from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class LicenseInfo(BaseModel):
    package_name: str
    license_type: Optional[str] = None
    permissions: Optional[List[str]] = None
    limitations: Optional[List[str]] = None
    obligations: Optional[List[str]] = None


class LicenseReport(BaseModel):
    packages: List[LicenseInfo]
    resources_used: Optional[List[str]] = None


class GithubRepo(BaseModel):
    url: HttpUrl

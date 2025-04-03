from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str


# Create settings instance
settings = Settings(_env_file=".env")

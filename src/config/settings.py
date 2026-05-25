import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "support_triage_db")
    MONGO_TICKET_COLLECTION: str = os.getenv("MONGO_TICKET_COLLECTION", "tickets")

    # LLM
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))

    # App
    APP_NAME: str = "Customer Support Triage AI"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    # AWS
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    SQS_QUEUE_URL: str = os.getenv("SQS_QUEUE_URL", "")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    
settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    example_data: str
    prompt_path: str
    prompt_version: str

    azure_openai_model: str
    azure_openai_api_key: str

    service_bus_connection_string: str
    service_bus_topic: str = "invoices"
    service_bus_subscription: str = "invoiceflow"

    blob_storage_connection_string: str
    blob_storage_container: str = "invoices"


settings = Settings()

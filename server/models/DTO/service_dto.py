from pydantic import BaseModel

class ServiceDTO(BaseModel):
    service_id: int
    service_name: str
    description: str
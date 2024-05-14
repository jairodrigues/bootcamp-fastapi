from pydantic import BaseModel

class Assistant(BaseModel):
    name: str
    description: str
    interaction_example: str

import time
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.assistant import AssistantSchema

from ..utils.logger import logger
from app.models.assistant import Assistant

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"]
)


@router.get("/")
async def get_assistants(db: Session = Depends(get_db)):
    try:
        assistants = db.query(AssistantSchema).all()
        return assistants
    except Exception as ex:
        logger.error(f"Request failed: Error {ex}")
        return JSONResponse(content={"success": False}, status_code=500)
    
@router.post("/")
async def create_assistant(assistant_data: Assistant, db: Session = Depends(get_db)):
    try:
        timestampt_now = datetime.fromtimestamp(int(time.time()))        
        assistant = AssistantSchema(
            name=assistant_data.name, 
            description=assistant_data.description, 
            interaction_example=assistant_data.interaction_example, 
            updated_at=timestampt_now,
            created_at=timestampt_now
        )
        db.add(assistant)
        db.commit()
        db.refresh(assistant)
        return JSONResponse(content={ 
            "name": assistant.name, 
            "description": assistant.description,
            "interaction_example": assistant.interaction_example
        }, 
        status_code=200)
    except Exception as ex:
        logger.error(f"Request failed: Error {ex}")
        return JSONResponse(content={"success": False}, status_code=500)

@router.patch("/{assistant_id}")
async def update_assistant(assistant_id: int, update_data: Assistant, db: Session = Depends(get_db)):
    assistant = db.query(AssistantSchema).filter(AssistantSchema.id == assistant_id).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    
    assistant.name = update_data.name if update_data.name else assistant.name
    assistant.description = update_data.description if update_data.description else assistant.description
    assistant.interaction_example = update_data.interaction_example if update_data.interaction_example else assistant.interaction_example
    assistant.updated_at = datetime.fromtimestamp(int(time.time()))

    db.commit()
    db.refresh(assistant)
    return JSONResponse(content={
        "name": assistant.name,
        "description": assistant.description,
        "interaction_example": assistant.interaction_example
    }, status_code=200)

@router.delete("/{assistant_id}")
async def delete_assistant(assistant_id: int, db: Session = Depends(get_db)):
    assistant = db.query(AssistantSchema).filter(AssistantSchema.id == assistant_id).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    
    db.delete(assistant)
    db.commit()
    return JSONResponse(content={"message": "Assistant deleted"}, status_code=200)
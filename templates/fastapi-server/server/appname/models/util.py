import uuid
from sqlalchemy import UUID, Column, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Type, TypeVar, Optional, List
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class TimeStampModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    datetime_created = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    last_edited = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

T = TypeVar('T')

class BaseManager:
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, obj_id: UUID) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, obj_in: BaseModel) -> T:
        db_obj = self.model(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, obj_id: UUID, obj_in: BaseModel) -> Optional[T]:
        db_obj = self.get_by_id(obj_id)
        if db_obj:
            for field, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_obj, field, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: UUID) -> bool:
        db_obj = self.get_by_id(obj_id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
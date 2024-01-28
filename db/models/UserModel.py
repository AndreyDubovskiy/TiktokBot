from db.models.BaseModel import BaseModel
from db.models.imports import *

class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))
    tg_name: Mapped[str] = mapped_column(String(255))
    events: Mapped[List["EventModel"]] = relationship("EventModel", back_populates="user")


    def __init__(self, tg_id: str, tg_name: str):
        self.tg_id = tg_id
        self.tg_name = tg_name

    def __repr__(self):
        return f"<UserModel(id={self.id}, tg_id={self.tg_id}, tg_name={self.tg_name})>"
from db.models.BaseModel import BaseModel
from db.models.imports import *


class EventModel(BaseModel):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="events")
    date_event = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"<EventModel(id={self.id}, name={self.name}, user_id={self.user_id})>"
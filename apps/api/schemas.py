from pydantic import BaseModel, EmailStr, ConfigDict


class SubscriptionCreate(BaseModel):
    email: EmailStr
    event_url: str


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    active: bool
    model_config = ConfigDict(from_attributes=True)

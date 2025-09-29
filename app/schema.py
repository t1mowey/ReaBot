from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    t_id: int

    class Config:
        from_attributes = True
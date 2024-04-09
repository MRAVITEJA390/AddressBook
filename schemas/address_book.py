from pydantic import BaseModel, Field


class AddressBookBase(BaseModel):
    name: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90, error_message="should be between 90 and -90")
    longitude: float = Field(ge=-180, le=180)


class AddressBookCreate(AddressBookBase):
    pass


class AddressBookUpdate(AddressBookBase):
    pass


class AddressBookDetail(AddressBookBase):
    id: int

    class Config:
        orm_mode = True


class AddressCoordinates(BaseModel):
    latitude: float = Field(ge=-90, le=90, error_message="should be between 90 and -90")
    longitude: float = Field(ge=-180, le=180)


class AddressWithDistance(AddressBookBase):
    id: int
    distance: float

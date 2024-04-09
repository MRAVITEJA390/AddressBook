from fastapi import APIRouter, Depends, HTTPException
from geopy.distance import great_circle
from sqlalchemy.orm import Session

from database import Base, engine
from dependencies import get_db
from models import AddressBook
from schemas import (AddressBookCreate, AddressBookDetail, AddressBookUpdate,
                     AddressCoordinates, AddressWithDistance)

router = APIRouter(prefix="/api/v1")

Base.metadata.create_all(engine)

ADDRESS_NOT_FOUND_MSG = "address with given id {} not found"


@router.post("/address_book/", response_model=AddressBookDetail)
async def create_address(address: AddressBookCreate, db: Session = Depends(get_db)):
    new_address = AddressBook(**address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@router.get("/address_book/", response_model=list[AddressBookDetail])
async def get_addresses(db: Session = Depends(get_db)):
    return db.query(AddressBook).all()


@router.get("/address_book/{address_id}/", response_model=AddressBookDetail)
async def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    address = db.query(AddressBook).filter(AddressBook.id == address_id).first()
    if address is None:
        raise HTTPException(
            status_code=404, detail=ADDRESS_NOT_FOUND_MSG.format(address_id)
        )

    return address


@router.post("/address_book/{address_id}/", response_model=AddressBookDetail)
async def update_address(
    address_id: int, address_info: AddressBookUpdate, db: Session = Depends(get_db)
):
    address = db.query(AddressBook).filter(AddressBook.id == address_id).first()
    if address is None:
        raise HTTPException(
            status_code=404, detail=ADDRESS_NOT_FOUND_MSG.format(address_id)
        )

    for column, val in address_info.dict().items():
        setattr(address, column, val)

    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.delete("/address_book/{address_id}")
async def delete_address(address_id: int, db: Session = Depends(get_db)) -> dict:
    address = db.query(AddressBook).filter(AddressBook.id == address_id).first()
    if address is None:
        raise HTTPException(
            status_code=404, detail=ADDRESS_NOT_FOUND_MSG.format(address_id)
        )

    db.delete(address)
    db.commit()
    return {"detail": "address {} deleted successfully".format(address_id)}


@router.post(
    "/addresses/within_distance/{distance}/", response_model=list[AddressWithDistance]
)
async def get_addresses_within_distance(
    distance: float, coordinates: AddressCoordinates, db: Session = Depends(get_db)
):
    addresses = db.query(AddressBook).all()
    addresses_within_distance = []
    coordinates_dict = coordinates.dict()
    location = (coordinates_dict["latitude"], coordinates_dict["longitude"])
    for address in addresses:
        address_location = (address.latitude, address.longitude)
        distance_diff = great_circle(location, address_location).kilometers

        if distance_diff <= distance:
            addresses_within_distance.append(
                AddressWithDistance(
                    id=address.id,
                    name=address.name,
                    latitude=address.latitude,
                    longitude=address.longitude,
                    distance=distance_diff,
                )
            )

    return addresses_within_distance

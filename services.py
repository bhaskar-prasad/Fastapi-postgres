import database as _database
import models as _models
import schemas as _schemas
from sqlalchemy.orm import Session
from typing import List

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_contact(contact:_schemas.CreateContact,db:"Session")->_schemas.Contact:
    contact = _models.Contact(**contact.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return _schemas.Contact.from_orm(contact)

async def get_contact(contact_id:int,db:"Session")->_schemas.Contact:
    contact = db.query(_models.Contact).get(contact_id)
    return _schemas.Contact.from_orm(contact)

async def get_contacts(db:"Session")->List[_schemas.Contact]:
    contacts = db.query(_models.Contact).all()
    return list(map(_schemas.Contact.from_orm,contacts))

async def update_contact(contact_id:int,contact:_schemas.CreateContact,db:"Session")->_schemas.Contact:
    contacts = db.query(_models.Contact).filter(_models.Contact.id==contact_id).first()
    contacts.first_name = contact.first_name
    contacts.last_name = contact.last_name
    contacts.email = contact.email
    contacts.phone_number = contact.phone_number
    db.commit()
    db.refresh(contacts)
    return _schemas.Contact.from_orm(contacts)

async def delete_contact(contact_id:int,db:"Session")->_schemas.Contact:
    contact = db.query(_models.Contact).get(contact_id)
    db.delete(contact)
    db.commit()
    return _schemas.Contact.from_orm(contact)
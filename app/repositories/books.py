from app.database import db
from bson import ObjectId
from datetime import datetime, timezone

books_collection = db["books"]


def create_book(book_data: dict):

    book_data["created_at"] = datetime.now(timezone.utc)

    result = books_collection.insert_one(book_data)

    book_data["_id"] = str(result.inserted_id)

    return book_data


def get_all_books():

    books = list(
        books_collection.find()
    )

    for book in books:
        book["_id"] = str(book["_id"])

    return books


def get_book_by_id(book_id: str):

    book = books_collection.find_one(
        {
            "_id": ObjectId(book_id)
        }
    )

    if not book:
        return None

    book["_id"] = str(book["_id"])

    return book


def update_book(book_id: str, book_data: dict):

    books_collection.update_one(
        {
            "_id": ObjectId(book_id)
        },
        {
            "$set": book_data
        }
    )

    return get_book_by_id(book_id)


def delete_book(book_id: str):

    result = books_collection.delete_one(
        {
            "_id": ObjectId(book_id)
        }
    )

    return result.deleted_count > 0
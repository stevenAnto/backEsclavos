from app.database import db
from bson import ObjectId

classifications_collection = db["classifications"]


def create_classification(data: dict):

    data["book_id"] = None

    result = classifications_collection.insert_one(data)

    data["_id"] = str(result.inserted_id)

    return data


def get_all_classifications():

    classifications = list(
        classifications_collection.find()
    )

    for item in classifications:
        item["_id"] = str(item["_id"])

    return classifications


def get_classification_by_id(classification_id: str):

    classification = classifications_collection.find_one(
        {
            "_id": ObjectId(classification_id)
        }
    )

    if not classification:
        return None

    classification["_id"] = str(classification["_id"])

    return classification


def update_classification(classification_id: str, data: dict):

    classifications_collection.update_one(
        {
            "_id": ObjectId(classification_id)
        },
        {
            "$set": data
        }
    )

    return get_classification_by_id(classification_id)


def delete_classification(classification_id: str):

    result = classifications_collection.delete_one(
        {
            "_id": ObjectId(classification_id)
        }
    )

    return result.deleted_count > 0

def get_available_classifications():

    classifications = list(
        classifications_collection.find(
            {
                "book_id": None
            }
        )
    )

    for item in classifications:
        item["_id"] = str(item["_id"])

    return classifications

def assign_book(classification_id: str, book_id: str):

    classifications_collection.update_one(
        {
            "_id": ObjectId(classification_id)
        },
        {
            "$set": {
                "book_id": book_id
            }
        }
    )

    return get_classification_by_id(classification_id)

def remove_book(classification_id: str):

    classifications_collection.update_one(
        {
            "_id": ObjectId(classification_id)
        },
        {
            "$set": {
                "book_id": None
            }
        }
    )

    return get_classification_by_id(classification_id)

def get_book_classifications(book_id: str):

    classifications = list(
        classifications_collection.find(
            {
                "book_id": book_id
            }
        )
    )

    for item in classifications:
        item["_id"] = str(item["_id"])

    return classifications

def get_book_total_records(book_id: str):

    pipeline = [
        {
            "$match": {
                "book_id": book_id
            }
        },
        {
            "$group": {
                "_id": None,
                "total": {
                    "$sum": "$record_count"
                }
            }
        }
    ]

    result = list(
        classifications_collection.aggregate(pipeline)
    )

    if not result:
        return 0

    return result[0]["total"]
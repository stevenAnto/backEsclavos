from bson import ObjectId

from app.database import db
from datetime import datetime, timezone


records_collection = db["records"]


def create_record(record_data: dict):

    result = records_collection.insert_one(record_data)

    record_data["_id"] = str(result.inserted_id)

    return record_data

def get_total_by_user(user_id: str):

    pipeline = [

        {
            "$match": {
                "user_id": user_id
            }
        },

        {
            "$group": {
                "_id": None,
                "total": {
                    "$sum": "$value"
                },
                "cantidad_registros": {
                    "$sum": 1
                }
            }
        }

    ]


    result = list(
        records_collection.aggregate(pipeline)
    )


    if not result:
        return {
            "total": 0,
            "cantidad_registros": 0
        }


    return {
        "total": result[0]["total"],
        "cantidad_registros": result[0]["cantidad_registros"]
    }

from app.database import db

users_collection = db["users"]


def get_all_users_summary():

    users = list(users_collection.find())

    result = []

    for user in users:

        summary = get_total_by_user(
            str(user["_id"])
        )

        result.append({

            "name": user.get("name"),

            "email": user.get("email"),

            "total": summary["total"],

            "cantidad_registros": summary["cantidad_registros"]

        })

    return result

def get_user_records(user_id: str):

    records = list(
        records_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("created_at", -1)
    )

    return records

def create_records(records):
    if not records:
        return 0

    result = records_collection.insert_many(records)

    return len(result.inserted_ids)

def delete_all_records():
    result = records_collection.delete_many({})
    return result.deleted_count

def update_record_value(record_id: str, value: int):

    print("========== REGISTROS ==========")

    records = records_collection.find(
        {},
        {
            "_id": 1,
            "user_id": 1,
            "user_email": 1,
            "value": 1
        }
    )

    for record in records:
        print(record)

    print("================================")

    result = records_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": {"value": value}}
    )

    print("matched_count:", result.matched_count)
    print("modified_count:", result.modified_count)

    return result
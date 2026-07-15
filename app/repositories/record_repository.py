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
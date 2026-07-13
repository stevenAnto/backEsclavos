from datetime import datetime

from app.database import users_collection


def get_user_by_email(email: str):

    return users_collection.find_one(
        {
            "email": email
        }
    )



def create_user(user_data: dict):

    result = users_collection.insert_one(user_data)

    user_data["_id"] = result.inserted_id

    return user_data



def update_last_login(email: str):

    users_collection.update_one(
        {
            "email": email
        },
        {
            "$set": {
                "last_login": datetime.utcnow()
            }
        }
    )
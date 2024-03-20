import json


def get_user_reputation(user_id, user_reputations):
    username = str(user_id)
    if username not in user_reputations:
        user_reputations[username] = {"reputation": 0, "history": []}
    return user_reputations[username]["reputation"]

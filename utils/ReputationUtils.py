import json


def get_user_reputation(user_id, user_reputations):
    username = str(user_id)
    if username not in user_reputations:
        user_reputations[username] = {"reputation": 0, "history": []}
    return user_reputations[username]["reputation"]


def get_trust_level(user_id, user_reputations):
    rep = get_user_reputation(user_id, user_reputations)
    if rep >= 10:
        return "trusted"
    elif -9 <= rep <= 9:
        return "neutral"
    else:
        return "untrusted"


def check_trusted(user_id, user_reputations):
    rep = get_user_reputation(user_id, user_reputations)
    return get_trust_level(rep) == "trusted"


def check_neutral(user_id, user_reputations):
    rep = get_user_reputation(user_id, user_reputations)
    return get_trust_level(rep) == "neutral"


def check_untrusted(user_id, user_reputations):
    rep = get_user_reputation(user_id, user_reputations)
    return get_trust_level(rep) == "untrusted"


def clear_reputation_history(user_id, user_reputations):
    username = str(user_id)
    if username in user_reputations:
        user_reputations[username]["history"] = []


def set_reputation(user_id, value, user_reputations):
    username = str(user_id)
    if username not in user_reputations:
        user_reputations[username] = {"reputation": 0, "history": []}
    user_reputations[username]["reputation"] = value


def get_reputation_history(user_id, user_reputations):
    username = str(user_id)
    if username not in user_reputations:
        user_reputations[username] = {"reputation": 0, "history": []}
    return user_reputations[username]["history"]

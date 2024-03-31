import os

# Environment variables
api_url = os.getenv('API_URL')
bot_token = os.getenv('BOT_TOKEN')

# Fixed values
paypal_email = "cvs0_main@proton.me"
randomNumberChannel = 1221152330699767808
reviewChannel = 1221152392427601940
ratingsChannel = 1221152588926423130
marketplaceChannel = 1221151839504961686
marketplaceRepChannel = 1221151819896459396

# Data paths
order_history_path = "data/order_history.txt"
products_path = "data/products.json"
carts_path = "data/carts.json"
reputation_path = "data/user_reputations.json"

# Configuration flags
debug = True
order_history = False
save_carts = False
ratings = True
marketplace = True

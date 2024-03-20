import os

# Environment variables
api_url = os.getenv('API_URL')
bot_token = os.getenv('BOT_TOKEN')

# Fixed values
paypal_email = "convexshop@proton.me"
randomNumberChannel = 1210028551378837556
reviewChannel = 1209661560562126878
ratingsChannel = 1218379961392562282
marketplaceChannel = 1219835017526775958
marketplaceRepChannel = 1219835432632582165

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

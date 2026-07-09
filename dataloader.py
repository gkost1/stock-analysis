import os

import finnhub
from dotenv import load_dotenv

load_dotenv()

finnhub_client = finnhub.Client(api_key=os.environ["FINNHUB_API_KEY"])
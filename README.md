# AzsTeleBot
Fuel Prices Telegram Bot 🚗💰

This Telegram bot provides up-to-date fuel prices for various cities across Russia. Users can select a city and retrieve the latest fuel prices, making it easier to find the best deals on gasoline, diesel, and other fuel types.

Features 🌟

- City Selection: Choose from a list of over 80 cities to get fuel prices.
- Fuel Price Information: Get the latest prices for different types of fuel, including the name and address of the gas station offering the lowest prices.
- Easy to Use: Simple command-based interface for ease of use.

Installation 🛠️

To install and run this bot, you'll need Python 3.6 or later and pip installed on your computer.

1. Clone the repository

git clone https://github.com/rokoss21/AzsTeleBot.git
cd AzsTeleBot

2. Install Dependencies

Install the required Python packages using pip:

pip install requests beautifulsoup4 python-telegram-bot

3. Set Up Telegram Bot

Create a new bot via BotFather on Telegram and get your API token. Replace the placeholder in the script with your actual token:

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

Running the Bot 🚀

To start the bot, simply run the script with Python:

python AzsTeleBot.py

Commands 📝

- /start: Begin interaction with the bot and select your city.
- /fuel: After selecting a city, use this command to fetch the latest fuel prices.

How It Works 🛠

1. Choose Your City: After starting the bot, you'll be prompted to select your city by sending the number associated with it.
2. Get Fuel Prices: Once you've chosen your city, use the /fuel command to see the lowest fuel prices in your selected city.

Contributing 🤝

Feel free to fork this repository, make changes, and submit pull requests if you have ideas on how to improve the bot or add new features.

License 📜

This project is open-source and available under the MIT License.

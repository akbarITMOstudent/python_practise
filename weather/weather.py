import os
import httpx
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
geolocator = Nominatim(user_agent="weather_report_bot")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, type the name of the city, and I will show you the weather. \n\n"
        "As example: Tashkent, Moscow, Saint-Petersburg"
    )

def get_coordinates(city: str):
    location = geolocator.geocode(city)

    if not location:
        return None
    
    return {
        "name": location.address,
        "lat": location.latitude,
        "lon": location.longitude
    }

async def get_weather(lat: float, lon: float):
    # Добавлен знак ? и относительная влажность в параметр current
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

async def weather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()

    await update.message.reply_text("I'm looking for a forecast......")

    try:
        coords = get_coordinates(city)

        if coords is None:
            await update.message.reply_text("City not found. Try again.")
            return
        
        data = await get_weather(coords["lat"], coords["lon"])
        current = data["current"]

        text = (
            f"City: {coords['name']}\n\n"
            f"Temp: {current['temperature_2m']}°C\n\n"
            f"Humidity: {current['relative_humidity_2m']}%\n\n"
            f"Wind speed: {current['wind_speed_10m']} km/h\n"
        )
        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text("Error, try later")
        print(f"Error: {e}")

def main():
    # Добавлены скобки () к .build()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
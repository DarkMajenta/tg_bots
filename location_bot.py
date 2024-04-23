import logging
from telegram import Update, InputMediaLocation
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.location import Location
import googlemaps

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Replace YOUR_BOT_TOKEN with your actual bot token
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)

# Replace YOUR_GOOGLE_API_KEY with your actual Google API key
gmaps = googlemaps.Client(key='YOUR_GOOGLE_API_KEY')

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Please share your location with me.')

def location(update: Update, context: CallbackContext):
    """Send the user's location on a map."""
    location = update.message.location
    context.bot.send_location(chat_id=update.effective_chat.id, latitude=location.latitude, longitude=location.longitude)

def route(update: Update, context: CallbackContext):
    """Calculate a route and send it to the user."""
    if len(context.args) < 1:
        update.message.reply_text('Please provide an end point for the route.')
        return

    end_point = context.args[0]

    user_location = update.message.location

    if not user_location:
        update.message.reply_text('Please share your location with me.')
        return

    directions_result = gmaps.directions(user_location.latitude,
                                      user_location.longitude,
                                      end_point,
                                      mode="driving",
                                      departure_time="now")

    if not directions_result:
        update.message.reply_text('Could not calculate a route.')
        return

    route_steps = directions_result[0]['legs'][0]['steps']

    route_text = ''
    for step in route_steps:
        route_text += f"{step['html_instructions'].replace('<b>', '').replace('</b>', '')}\n"

    update.message.reply_text(route_text, parse_mode='HTML')
    update.message.reply_text('Share this route:', reply_markup=InputMediaLocation(latitude=directions_result[0]['legs'][0]['start_location']['lat'],
                                                                                   longitude=directions_result[0]['legs'][0]['start_location']['lng']))                                                                                   longitude=directions_result[0]['legs'][0]['start_location']['lng']))

def main():
    """Start the bot."""
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, location))
    dp.add_handler(CommandHandler("route", route, pass_args=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    'start_webhook' does not work in the background.
    updater.idle()

if __name__ == '__main__':
    main()

import sys
import random
import string
import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from flesch_kincaid import FleschKincaid
import telebot

# Replace YOUR_WORDPRESS_URL, YOUR_USERNAME, and YOUR_PASSWORD with your actual WordPress credentials
wp = Client('http://YOUR_WORDPRESS_URL/xmlrpc.php', 'YOUR_USERNAME', 'YOUR_PASSWORD')

# Replace YOUR_TELEGRAM_BOT_TOKEN with your actual Telegram bot token
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

def generate_paragraph(topic):
    """Generate a paragraph using the Easy GPT Content API."""
    # Replace YOUR_EASY_GPT_CONTENT_API_KEY with your actual Easy GPT Content API key
    headers = {
        'Authorization': 'Bearer YOUR_EASY_GPT_CONTENT_API_KEY'
    }
    params = {
        'topic': topic,
        'length': 200
    }
    response = requests.post('https://api.easygptcontent.com/v1/generate', headers=headers, params=params)
    return response.json()['content']

def validate_text(text):
    """Validate the text using the Flesch-Kincaid readability test and grammar check."""
    fk = FleschKincaid()
    score = fk.calculate(text)
    if score < 60:
        return False, 'The text is too difficult to read. Please simplify it.'
    grammar_check_url = 'https://api.grammarbot.io/v2/check'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'language': 'en-US',
        'text': text
    }
    response = requests.post(grammar_check_url, headers=headers, json=data)
    if response.json()['result']['score'] < 0.8:
        return False, 'The text contains grammar errors. Please correct them.'
    return True, ''

def publish_article(title, content):
    """Publish an article to WordPress."""
    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = 'publish'
    wp.call(NewPost(post))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send a welcome message when the bot is started."""
    bot.reply_to(message, 'Hello! Send me a topic to generate an article.')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Generate and publish an article to WordPress."""
    # Generate a random title
    title = ' '.join(random.choices(string.ascii_lowercase, k=5)).title()

    # Generate the content
    content = ''
    for i in range(10):
        paragraph = generate_paragraph(message.text)
        content += paragraph + '\n\n'

    # Validate the text
    is_valid, message = validate_text(content)
    if not is_valid:
        bot.reply_to(message, message)
        return

    # Publish the article
    publish_article(title, content)
    bot.reply_to(message, 'Article published successfully.')

if __name__ == '__main__':
    bot.polling()

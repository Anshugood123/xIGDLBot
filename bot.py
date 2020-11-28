#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
# Coded with ❤️ by Neranjana Prasad (@NandiyaLive)

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
import requests
from bs4 import BeautifulSoup as bs

bot_token = ""


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Instagram Media Downloader Bot.\nPlease note that this is still on beta stage.\n\nPlease leave a feedback on @NandiyaThings Support Chat.", parse_mode=telegram.ParseMode.HTML)


def help(update, context):
    update.message.reply_text('''/stories username - Download stories from the username’s profile.\n/feed username - Download images & videos from the username’s feed.\n\n<b>How to find the username?</b>\nOpen Instagram app & then go to the profile that you want to download. Username must be on the top.\nIn case you are using a browser you can find it in the Address bar.\n<b>Example : </b>Username for instagram.com/rashmika_mandanna & @rashmika_mandanna is 'rashmika_mandanna' 😉''')


def about(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='''This bot can help you to download media from Instagram without leaving Telegram.\nMade with ❤️ + python-telegram-bot\nSource Code : <a href="https://github.com/NandiyaLive/xIGDLBot">GitHub</a>''', parse_mode=telegram.ParseMode.HTML)


def stories(update, context):
    status_page = "https://www.insta-stories.com/en/status"

    req_status = requests.get(status_page).text
    status = bs(req_status, "lxml")

    if status.find("div", class_="status status--ok"):
        fullmsg = update.message.text
        
        if fullmsg == "/stories":
            update.message.reply_text('/stories [instagram username]\nPlease read /help')
        else :
            msg = fullmsg.replace("/stories ", "")
            chat_id = update.message.chat_id

            if "@" in msg.lower():
                query = msg.replace("@", "")
            else:
                query = msg

            url = f"https://www.insta-stories.com/en/stories/{query}"
            r = requests.get(url).text

            soup = bs(r, "lxml")

            if soup.find("div", class_="msg msg-user-not-found"):
                update.message.reply_text(
                    "This username doesn't exist. Please try with another one.")

            else:
                if soup.find("div", class_="msg msg-no-stories"):
                    update.message.reply_text(
                        "No stories available. Please try again later.")

                else:
                    try:
                        profile = soup.find("div", class_="user-name").text
                        update.message.reply_text(
                            f"Downloading stories of {profile}")

                        videos = soup.findAll(class_='story-video')
                        photos = soup.findAll(class_='story-image')

                        for video in videos:
                            context.bot.send_video(
                                chat_id=update.message.chat_id, video=video['src'])

                        for photo in photos:
                            context.bot.send_photo(
                                chat_id=update.message.chat_id, photo=photo['src'])
                    except:
                        context.bot.send_message(chat_id=update.message.chat_id,
                                                 text="Something went wrong. Please try again later.", parse_mode=telegram.ParseMode.HTML)

    else:
        update.message.reply_text(
            "API is not working. Please try again later.")


def instadp(query, chat_id):
    bot = telegram.Bot(token=bot_token)

    url = f"https://www.instadp.com/stories/{query}"
    r = requests.get(url).text

    soup = bs(r, "lxml")
    try:
        profile = soup.find("div", class_="call-to-action").text

        bot.send_message(
            chat_id, text=f"Downloading stories of {profile}")
        for items in soup:
            url = soup.find("img", class_="download-btn")["src"]

        bot.send_document(chat_id=chat_id, document=url)

    except:
        bot.send_message(
            chat_id, text="Something went wrong. Please try again later.")

def echo(update, context):
    update.message.reply_text('Please read /help')


def main():
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    dp.add_handler(CommandHandler("stories", stories, run_async=True))
    dp.add_handler(CommandHandler("about", about, run_async=True))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
from flask import request
from FBBlib.fbbot import FBBot
from FBBlib.order import FBOrder
from FBBlib.attachment import FBAttachment
from FBBlib.AirlineFlightUpdate import AirlineFlightUpdate
from FBBlib.AirlineCheckin import AirlineCheckin

import json

token = "EAADKNpJZBx5YBAEVn6aKJl735RYd6xyNm5Qf6bJG7seFVO9aZBQ1uqO6zpTOVkAW4haQPiSeqvmtsZCZCgzSk3e1UUCCz02G4KfrGbFYWzpPrWhFGZAQR5GGhZAjJ3ByhU2n6F5dGK1Q6IE7lT6jsTGY8EVIf6ikJyVB4cu6MdiQZDZD"
verify_token = "customtoken228"
bot = FBBot(token, verify_token)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    return bot.webhook(request, on_message, on_postback, on_linked, on_unlinked)

def on_linked(sender, login, requestInfo):
    print("link")
    print(sender+" "+ login)

def on_unlinked(sender, requestInfo):
    print("unlink")
    print(sender+" unlink")

def on_postback(sender, text, requestInfo):
    print("post")
    if (text == "USER_YES_PAYLOAD"):
        send_quick_replies(bot, sender)
    elif (text == "USER_BACK_PAYLOAD"):
        send_buttons(bot, sender)
    else:
        bot.send_text_message(sender, "Feel free to write me anytime :)")


def on_message(sender, text, requestInfo):
    print("message")
    send_repeat_buttons = True
    if(text == "Video"):
        bot.send_message_file_attachment(sender, FBAttachment.File.video, "http://img-9gag-fun.9cache.com/photo/adXLy8N_460sv.mp4")
    elif (text == "Image"):
        bot.send_message_file_attachment(sender, FBAttachment.File.image,
                                         "http://img-9gag-fun.9cache.com/photo/aEnxQve_460s_v1.jpg")
    elif (text == "Generic"):
        buttons = [
            {
                "type": "web_url",
                "url": "https://www.google.com",
                "title": "View Google",

            },
            {
                "type": "web_url",
                "url": "https://www.yandex.com",
                "title": "View Yandex",

            },
            {
                "type": "postback",
                "title": "Back",
                "payload": "USER_BACK_PAYLOAD"
            }
        ]
        bot.send_message_generic(sender, "Search engines' catalogue", "Select any",
                                 "https://www.24k.com.sg/images/sem1.png",
                                 buttons)
        send_repeat_buttons = False
    elif (text == "File"):
        bot.send_message_file_attachment(sender, FBAttachment.File.file,
                                         "http://ntarasov.ru/files/nezach.pdf")
    elif(text == "Receipt"):
        message = FBOrder(
            "Stephane Crozatier",
            "125352345",
            "USD",
            "Visa",
            [
                FBOrder.one_purchase("T-Shirt", 1,"yellow", 5, "USD", "http://cdn01.shopclues.net/images/detailed/19936/yellowtshirt_1434534567.jpg"),
                FBOrder.one_purchase("Baseball cap", 2,"white",  2, "USD", "http://i01.i.aliimg.com/img/pb/630/860/383/383860630_626.jpg")
            ],
            FBOrder.price_summary(9, 0, 1, 8),
            "http://google.com",
            FBOrder.address("1 Hacker Way", "", "Menlo Park", "94025", "CA", "US"),
            "427561765",
            [
                FBOrder.price_one_adjustment("2$ Off coupon", 2)
            ]
        )
        bot.send_message_TypeC(sender, message)
    elif text == "My Info":
        resp = bot.get_userinfo(sender)
        message = "{0} {1}\nGender:{2}\nLocale:{3}\nTimezone:{4}".format(resp["first_name"],
                                                                                               resp["last_name"],
                                                                                               resp["gender"],
                                                                                               resp["locale"],
                                                                                               resp["timezone"])
        bot.send_text_message(sender, message)
        bot.send_message_file_attachment(sender, FBAttachment.File.image, resp["profile_pic"])
    elif (text == "FirstAirline"):
        message = AirlineCheckin(
            "Checkin",
            "ru_RU",
            "12356",
            [
                AirlineCheckin.make_flight_info(
                    "4142",
                    AirlineCheckin.make_airport("SIN", "Singapore"),
                    AirlineCheckin.make_airport("DME", "Moscow"),
                    AirlineCheckin.make_flight_schedule("2016-01-05T15:05", "2016-01-06T15:05")
                )
            ]
            , "https://google.com")
        bot.send_message_TypeC(sender, message)

    elif (text == "SecondAirline"):
        message = AirlineFlightUpdate(
            "UPD",
            "delay",
            "ru_RU",
            "12356",
            AirlineFlightUpdate.make_update_flight_info(
                "4142",
                AirlineFlightUpdate.make_airport("SIN", "Singapore"),
                AirlineFlightUpdate.make_airport("DME", "Moscow"),
                AirlineFlightUpdate.make_flight_schedule("2016-01-05T15:05", "2016-01-07T15:05")
            )
        )
        bot.send_message_TypeC(sender, message)
    else:
        send_repeat_buttons = False
        send_quick_replies(bot, sender)

    if send_repeat_buttons:
        send_buttons(bot, sender)


def send_quick_replies(bot, sender):
    bot.send_text_message(sender, "What can I help you?", [
        FBAttachment.quick_reply("Video"),
        FBAttachment.quick_reply("Image"),
        FBAttachment.quick_reply("Generic"),
        FBAttachment.quick_reply("Receipt"),
        FBAttachment.quick_reply("File"),
        FBAttachment.quick_reply("My Info"),
        FBAttachment.quick_reply("FirstAirline"),
        FBAttachment.quick_reply("SecondAirline")
    ])


def send_buttons(bot, sender):
    buttons = [
        {
            "type": "postback",
            "title": "Yes",
            "payload": "USER_YES_PAYLOAD"
        },
        {
            "type": "postback",
            "title": "No",
            "payload": "USER_NO_PAYLOAD"
        }
    ]
    bot.send_message_buttons(sender, "Repeat these steps again? :)", buttons)
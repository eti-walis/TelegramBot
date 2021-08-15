import random
from flask import Flask, Response, request
import requests
import api
import pandas as pd

items = ["dress", "skirt", "jackets", "shoes"]
colors = ["black", "white", "pink", "blue", "yellow", "green", "red", "purple", "orange"]
size = ["xs", "s", "m", "l", "xl"]

order = [0, 0, 0]
orders_dic = {}

TOKEN = "1959475327:AAFMUkOCTeqGBbBTR8AJN3gawaOHsgDaCmQ"
TELEGRAM_INIT_WEBHOOK_UR = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://fd36deadcb95.ngrok.io/message"
requests.get(TELEGRAM_INIT_WEBHOOK_UR)
app = Flask(__name__)
random.seed()


def init():
    for i in range(100):
        order = []
        order.append(random.choice(items))
        order.append(random.choice(colors))
        order.append(random.choice(size))
        order = str(order)
        if order in orders_dic:
            orders_dic[order] += 1
        else:
            orders_dic[order] = 1
    d = {'order': [], 'times': []}
    for k, v in orders_dic.items():
        d['order'].append(k)
        d['times'].append(v)

    new = pd.DataFrame(d)
    new.to_csv("shoppingBotReaserch.csv", index=False)


# return the most popular searches
def get_popular(dic, k=5):
    # Sort the given dictionary.
    d = {u: v for u, v in sorted(dic.items(), key=lambda item: item[1])}
    # return the first kth largest elements in list named lst
    lst = []
    for item in d:
        x = item.split(", ")
        str = x[0][:-1] + " " + x[1][1:]  # category, color
        if str not in lst and len(lst) < k:
            lst.append(str[2:-1])
    mystr = ""
    for i in range(k):
        mystr += lst[i] + '\n'
    return mystr


# return the links for the products and save the search in the dict
def get_url(order):
    if 0 in order:
        return "Welcome to the shopping bot, please enter category from: dress, skirt, jackets, shoes"
    kLinks = api.get_links(str(order[0]), str(order[1]), str(order[2]))
    print(kLinks[0])
    order = str(order)
    if order in orders_dic:
        orders_dic[order] += 1
    else:
        orders_dic[order] = 1
    order = [0, 0, 0]
    return kLinks[0] + "\n" + kLinks[1] + "\n" + kLinks[2] + "\n" + kLinks[3] + "\n" + kLinks[4]


# Bot
@app.route("/message", methods=["POST"])
def handle_message() -> Response:
    """
    get the massage from the user and return a response
    :return: response
    """
    commend = request.get_json()["message"]["text"]

    if commend == "/start":
        txt = "Welcome to the shopping bot, please enter category from: dress, skirt, jackets, shoes, or type popular " \
              "to get the most popular searches "
    elif str(commend).lower() in items:
        order[0] = str(commend)
        txt = "choose color"
    elif str(commend).lower() in colors:
        if order[0] == 0:
            txt = "choose category"
        order[1] = str(commend)
        txt = "choose size"
    elif str(commend).lower() in size:
        order[2] = str(commend)
        txt = get_url(order)
    elif str(commend).lower() == "popular":
        txt = get_popular(orders_dic)
    else:
        txt = "try again"
        # print(orders_dic)
    chat_id = request.get_json()["message"]["chat"]["id"]
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={txt}")
    return Response("Success")


if __name__ == '__main__':
    init()
    #app.run(port=7002)

import other.creds as creds
from pybit import WebSocket, HTTP
import other.firebase as firebase
import talosLevers

timeInterval = talosLevers.timeInterval
fiatPerTrade = talosLevers.fiatPerTrade

# the api and secret key must be reset every three months

wsTickers = WebSocket(
    endpoint="wss://stream.bybit.com/realtime_public",
    subscriptions=[
        "candle.{}.BTCUSDT".format(timeInterval),
        "candle.{}.ETHUSDT".format(timeInterval),
        "candle.{}.LINKUSDT".format(timeInterval),
    ],
)
ws = WebSocket(
    endpoint="wss://stream.bybit.com/realtime_private",
    subscriptions=[
        "order",
        "position",
    ],
    api_key=creds.apiKey,
    api_secret=creds.privateKey,
)
session = HTTP(
    endpoint="https://api.bybit.com", api_key=creds.apiKey, api_secret=creds.privateKey
)


# lists to hold trade values
btcPredictProb = []
ethPredictProb = []
linkPredictProb = []
btcStop = []
ethStop = []
linkStop = []
btcTakeProfit = []
ethTakeProfit = []
linkTakeProfit = []


# need to find a way to update stop and prob values for the trade.  This will update on init and also after every model is run
def updateTradeValues():
    # clear lists
    btcPredictProb.clear()
    ethPredictProb.clear()
    linkPredictProb.clear()
    btcStop.clear()
    ethStop.clear()
    linkStop.clear()
    btcTakeProfit.clear()
    ethTakeProfit.clear()
    linkTakeProfit.clear()
    # btc
    print("updating btc trade values")
    btcPredictProb.append(firebase.db.child("BTC").child("predictProb").get().val())
    btcStop.append(firebase.db.child("BTC").child("stop").get().val())
    btcTakeProfit.append(firebase.db.child("BTC").child("takeProfit").get().val())
    # eth
    print("updating eth trade values")
    ethPredictProb.append(firebase.db.child("ETH").child("predictProb").get().val())
    ethStop.append(firebase.db.child("ETH").child("stop").get().val())
    ethTakeProfit.append(firebase.db.child("ETH").child("takeProfit").get().val())

    # link
    print("updating link trade values")
    linkPredictProb.append(firebase.db.child("LINK").child("predictProb").get().val())
    linkStop.append(firebase.db.child("LINK").child("stop").get().val())
    linkTakeProfit.append(firebase.db.child("LINK").child("takeProfit").get().val())





# trading logic


def tradeBTC(prediction):
    #min quantity has to be .001 for the trade to go through
    # long
    if prediction >= btcPredictProb[0]:
        price = wsTickers.fetch("candle.{}.BTCUSDT".format(timeInterval))["close"]
        longStopLoss = round(price - (price * linkStop[0]),4)
        longEntry = price - 0.5
        longTakeProfit = round(price + (price * linkTakeProfit[0]),4)
        qty = round(fiatPerTrade / price, 4)
        orders = [{"symbol": "BTCUSDT", "order_type": "Limit","side": "Buy",
            "qty": qty, "price": i,"stop_loss": longStopLoss,"take_profit": longTakeProfit, "time_in_force": "GoodTillCancel", 
            "close_on_trigger":False, "reduce_only":False,
            }for i in [longEntry]]
        session.place_active_order_bulk(orders)

    # short
    else:
        price = wsTickers.fetch("candle.{}.BTCUSDT".format(timeInterval))["close"]
        shortStopLoss = round(price - (price * linkStop[0]),4)
        shortEntry = price + 0.5
        shortTakeProfit = round(price - (price * linkTakeProfit[0]),4)
        qty = round(fiatPerTrade / price, 4)
        orders = [{"symbol": "BTCUSDT", "order_type": "Limit","side": "Sell",
            "qty": qty, "price": i,"stop_loss": shortStopLoss,"take_profit": shortTakeProfit, "time_in_force": "GoodTillCancel", 
            "close_on_trigger":False, "reduce_only":False,
            }for i in [shortEntry]]
        session.place_active_order_bulk(orders)


def tradeETH(prediction):
    # long
    if prediction >= ethPredictProb[0]:
        price = wsTickers.fetch("candle.{}.ETHUSDT".format(timeInterval))["close"]
        longStopLoss = round(price - (price * linkStop[0]),4)
        longEntry = price - 0.05
        longTakeProfit = round(price + (price * linkTakeProfit[0]),4)
        qty = round(fiatPerTrade / price, 4)
        orders = [{"symbol": "ETHUSDT", "order_type": "Limit","side": "Buy",
            "qty": qty, "price": i,"stop_loss": longStopLoss,"take_profit": longTakeProfit, "time_in_force": "GoodTillCancel", 
            "close_on_trigger":False, "reduce_only":False,
            }for i in [longEntry]]
        session.place_active_order_bulk(orders)


    # short
    else:
        price = wsTickers.fetch("candle.{}.ETHUSDT".format(timeInterval))["close"]
        shortStopLoss = round(price - (price * linkStop[0]),4)
        shortEntry = price + 0.05
        shortTakeProfit = round(price - (price * linkTakeProfit[0]),4)
        qty = round(fiatPerTrade / price, 4)
        orders = [{"symbol": "ETHUSDT", "order_type": "Limit","side": "Sell",
            "qty": qty, "price": i,"stop_loss": shortStopLoss,"take_profit": shortTakeProfit, "time_in_force": "GoodTillCancel", 
            "close_on_trigger":False, "reduce_only":False,
            }for i in [shortEntry]]
        session.place_active_order_bulk(orders)


def tradeLINK(prediction):
    # long
    if prediction >= linkPredictProb[0]:
        price = wsTickers.fetch("candle.{}.LINKUSDT".format(timeInterval))["close"]
        longStopLoss = round(price - (price * linkStop[0]),4)
        longEntry = price - 0.005
        longTakeProfit = round(price + (price * linkTakeProfit[0]),4)
        qty = round(fiatPerTrade / price, 4)
        orders = [{"symbol": "LINKUSDT", "order_type": "Limit","side": "Buy",
            "qty": qty, "price": i,"stop_loss": longStopLoss,"take_profit": longTakeProfit, "time_in_force": "GoodTillCancel", 
            "close_on_trigger":False, "reduce_only":False,
            }for i in [longEntry]]
        
        session.place_active_order_bulk(orders)

    # short
    else:
        price = wsTickers.fetch("candle.{}.LINKUSDT".format(timeInterval))["close"]
        shortStopLoss = round(price - (price * linkStop[0]),4)
        shortEntry = price + 0.005
        shortTakeProfit = round(price - (price * linkTakeProfit[0]),4)
        qty = round(fiatPerTrade / price, 4)
        orders = [{"symbol": "LINKUSDT", "order_type": "Limit","side": "Sell",
            "qty": qty, "price": i,"stop_loss": shortStopLoss,"take_profit": shortTakeProfit, "time_in_force": "GoodTillCancel", 
            "close_on_trigger":False, "reduce_only":False,
            }for i in [shortEntry]]
        session.place_active_order_bulk(orders)

        



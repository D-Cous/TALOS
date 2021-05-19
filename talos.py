from datetime import datetime
import talosMechanics as tm
import data.initTradingView as initTradingView
import trade.tradeAsset as trade
import talosLevers as tl

#main file
#Project TALOs (Technical Analysis Learning Algorithms)

print('Talos starting up')

#init
trade.updateTradeValues()
#set up models for predictions
tm.loadModels()

#run training/trading schedule
tm.scheduler()

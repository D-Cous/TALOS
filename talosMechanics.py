import data.downloadTrainingData as dlTD
import data.scrubProdData as scrubProdData
import trade.tradeMechanics as tradeMechanics
import data.scrubAndTrain as scrubAndTrain
from keras.models import load_model
import data.emailReport as email
import talosLevers as tl
import datetime
import other.firebase as fb

import data.downloadProductionData as dlPD
import trade.tradeAsset as trade

timeInterval = tl.timeInterval
models = []


def getTime():
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    day = datetime.datetime.now().day

    return {'hour': hour, 'minute':minute, 'day':day}

#load models on talos init
def loadModels():
    print('loading btc')
    btcModel = load_model('models/BTC.h5')
    print('loading eth')
    ethModel = load_model('models/ETH.h5')
    print('loading link')
    linkModel = load_model('models/LINK.h5')

    models.append(btcModel)
    models.append(ethModel)
    models.append(linkModel)


def talosModel():
    #download training data
    #-----------
    dlTD.dlTD()

    #scrub data and train models
    #-----------
    #ETH
    ethData = 'data/trainingData/KRAKEN_ETHUSD, {}.csv'.format(timeInterval)
    scrubAndTrain.scrubAndTrain(asset = 'ETH', file = ethData)
    #LINK
    linkData = 'data/trainingData/COINBASE_LINKUSD, {}.csv'.format(timeInterval)
    scrubAndTrain.scrubAndTrain(asset ='LINK', file =linkData)
    #BTC
    btcData = 'data/trainingData/BYBIT_BTCUSDT, {}.csv'.format(timeInterval)
    scrubAndTrain.scrubAndTrain(asset = 'BTC',  file =btcData)

    #update last model run time
    modelRunTime = getTime()
    fb.db.child('lastModelRunTime').set().val(modelRunTime['day'])


    #set new trading params
    #-----------
    btcReport = tradeMechanics.tradeMechanics('data/trainingData/btcResults.csv', asset='BTC')
    ethReport = tradeMechanics.tradeMechanics('data/trainingData/ethResults.csv',asset= 'ETH')
    linkReport = tradeMechanics.tradeMechanics('data/trainingData/linkResults.csv', asset = 'LINK')

    
    trade.updateTradeValues()

    #email morning report
    #-----------
    email.emailReport(ethReport=ethReport, linkReport=linkReport, btcReport=btcReport, timeInterval = timeInterval)

    


def talosTrade():
    #close all previous positions and unfilled orders
    #-----------
    trade.session.close_position('BTCUSDT')
    trade.session.close_position('ETHUSDT')
    trade.session.close_position('LINKUSDT')
    trade.session.cancel_all_active_orders()

    #download new instance data
    #-----------
    dlPD.dlPD()

    #scrub prediction data
    #-----------
    #ETH
    ethData = 'data/prodData/KRAKEN_ETHUSD, {}.csv'.format(timeInterval)
    ethScrub = scrubProdData.scrub(ethData)
    #LINK
    linkData = 'data/prodData/COINBASE_LINKUSD, {}.csv'.format(timeInterval)
    linkScrub = scrubProdData.scrub(linkData)
    #BTC
    btcData = 'data/prodData/BYBIT_BTCUSDT, {}.csv'.format(timeInterval)
    btcScrub = scrubProdData.scrub(btcData)


    #Predict each instance
    #-----------
    #BTC
    btcModel = models[0]
    btcPred = btcModel.predict(btcScrub)
    btcPred = btcPred[0][0]
    #ETH
    ethModel = models[1]
    ethPred = ethModel.predict(ethScrub)
    ethPred = ethPred[0][0]
    #LINK
    linkModel = models[2]
    linkPred = 'predfunctiongoeshere'
    linkPred = linkPred[0][0]
    
    #Run trade logic
    #-----------
    trade.tradeBTC(btcPred)
    trade.tradeETH(ethPred)
    trade.tradeLINK(linkPred)

    #Reset prodData 
    #-----------    
    dlPD.deleteProdData('data/prodData/KRAKEN_ETHUSD, {}.csv'.format(timeInterval))
    dlPD.deleteProdData('data/prodData/COINBASE_LINKUSD, {}.csv'.format(timeInterval))
    dlPD.deleteProdData('data/prodData/BYBIT_BTCUSDT, {}.csv'.format(timeInterval))



def getLastModelRunTime():
    try:
        fb.db.child('lastModelRunTime').get().val()
        return fb.db.child('lastModelRunTime').get().val()

    except:
        return 'not set'

    



#run scheduler
def scheduler():
    time = getTime()
    lastModelRunTime = getLastModelRunTime()
    if time['hour'] >= tl.runModelsTime and time['day'] is not lastModelRunTime:
        talosModel()
    if (time['minute'] % tl.timeInterval == 0):
        talosTrade()

    scheduler()

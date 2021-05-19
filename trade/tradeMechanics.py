import numpy as np
import pandas as pd
import numpy
import other.firebase as firebase
import datetime

def tradeMechanics(file,asset):
    

    rawresults = pd.read_csv(file).iloc[:, 1:]
    results = pd.read_csv(file).iloc[:, 1:].values

    probability = results[:, 0]
    groundTruths = results[:, 2]
    priceChange = results[:, 3]
    stopLow = results[:, 4]
    stopHigh = results[:, 5]


    # find the best pred prob to get the most right
    bestPredictionProb = 0
    bestCorrect = 0

    # test predict prob up to .99
    for x in range(100):
        correct = 0
        testProb = x / 100
        i = 0
        # for each prediction
        while i < len(probability):
            # if testprob is greater than the probability and ground truths is up add to correct
            if testProb > probability[i] and groundTruths[i] == 1:
                # add one to correct
                correct += 1
            # else, if testprob is less than prob and ground truths is down, add to correct
            elif testProb < probability[i] and groundTruths[i] == 0:
                correct += 1

            i += 1

        # print('testprob is ' + str(testProb) + ' and amount correct is' + str(correct))

        if correct >= bestCorrect:
            bestPredictionProb = testProb
            bestCorrect = correct


    print(
        "best predict probability is "
        + str(bestPredictionProb)
        + "with best correct at "
        + str(bestCorrect)
        + " out of "
        + str(len(probability))
        + " ("
        + str(bestCorrect / len(probability))
        + ")"
    )


    # find max take profit
    bestTakeProfitValue = 0
    bestTakeProfitHit = 0
    bestManualExit = 0

    # test each take profit value up to 3%
    for x in range(300):
        takeProfitHit = 0
        testTakeProfit = x / 100
        manualExit = 0

        z = 0
        while z < len(probability):
            priceChangeUp = stopHigh[z] + priceChange[z]
            priceChangeDown = (stopLow[z] * (-1)) + priceChange[z]

            # if the prediction is 1 and correct
            if (bestPredictionProb > probability[z] and groundTruths[z] == 1 and testTakeProfit <= priceChangeUp):
                takeProfitHit += 1
            # if correct pred 1 but doesnt hit the take profit
            elif (bestPredictionProb > probability[z] and groundTruths[z] == 1 and testTakeProfit > priceChangeUp):
                manualExit += 1
            # if the prediction is 0 and correct
            elif ( bestPredictionProb < probability[z] and groundTruths[z] == 0 and (testTakeProfit * (-1)) >= priceChangeDown):
                takeProfitHit += 1
            # if correct pred 0 but it doesnt hit the stop loss
            elif (bestPredictionProb < probability[z] and groundTruths[z] == 0 and (testTakeProfit * (-1)) < priceChangeDown):
                manualExit += 1
            z += 1

        if takeProfitHit > bestTakeProfitHit:
            bestTakeProfitHit = takeProfitHit
            bestTakeProfitValue = testTakeProfit
            bestManualExit = manualExit

    print(
        "best takeprofit is "
        + str(bestTakeProfitValue)
        + "with best take profit hit at "
        + str(bestTakeProfitHit)
        + " out of "
        + str(bestTakeProfitHit + bestManualExit)
    )
    # find best stop loss based on pandl
    def bestTradeValues(takeProfit, predictionProb, stop):
        stopLoss = stop * -1
        correctUp = 0
        correctDown = 0
        incorrectUp = 0
        incorrectDown = 0
        stopped = 0
        takeProfitHit = 0
        manualExit = 0

        pandl = []
        i = 1

        while i < len(probability):

        # if the pred is 1
            if predictionProb > probability[i]:
                # if the ground truth is 1 and prediction is correct
                if groundTruths[i] == 1:
                    # check if it gets stopped out
                    if stop <= stopLow[i]:
                        stopped += 1
                        pandl.append(stopLoss)
                    # if it doesnt get stopped out
                    else:
                        # if it hits take profit (the price goes past the take profit level)
                        if takeProfit <= priceChange[i] + stopHigh[i]:
                            takeProfitHit += 1
                            correctUp += 1
                            pandl.append(takeProfit)
                        # if it doesnt hit take profit, and executes market order manually
                        else:
                            manualExit += 1
                            correctUp += 1
                            pandl.append(priceChange[i])
                # if the prediction is 1 but the ground truth is 0
                elif groundTruths[i] == 0:
                    incorrectUp += 1
                    stopped += 1
                    pandl.append(stopLoss)
            # ----------------
            # if the pred is 0
            if predictionProb < probability[i]:
                # if the ground truth is 0 and the prediction is correct
                if groundTruths[i] == 0:
                    # check if it gets stopped out
                    if stop <= stopHigh[i]:
                        stopped += 1
                        pandl.append(stopLoss)
                    # if it doesnt get stopped out
                    else:
                        # if it hits take profit (the price goes past the take profit level)
                        if (takeProfit * (-1)) <= priceChange[i] + (stopLow[i] * (-1)):
                            takeProfitHit += 1
                            correctDown += 1
                            pandl.append(takeProfit)
                        else:
                            manualExit += 1
                            correctDown += 1
                            pandl.append((priceChange[i]) * (-1))
                elif groundTruths[i] == 1:
                    incorrectDown += 1
                    stopped += 1
                    pandl.append(stopLoss)
            i += 1

        finalPandl = 0
        z = 0
        while z < len(pandl):
            finalPandl += pandl[z]
            z += 1

        # add taker fees and maker rebates
        takerFee = -0.00075
        makerRebate = 0.00025

        # add taker fees to the manual exits and incorrect Ups and Downs (stop loss exits)
        finalPandl = finalPandl + ((stopped + incorrectDown) * takerFee)

        # add maker rebates to the entries and take profit exits
        totalEntries = correctUp + correctDown + incorrectUp + incorrectDown
        finalPandl = finalPandl + ((takeProfitHit + totalEntries) * makerRebate)

        return [finalPandl,stop,predictionProb,
            takeProfit,correctUp,incorrectUp,correctDown,incorrectDown,stopped,takeProfitHit,manualExit,]
    pandl = 0
    bestStop = 0

    # checking best stop value based on pandl, stop goes up to .99
    for x in range(1,100):
        stop = x / 100
        val = bestTradeValues(
            takeProfit=bestTakeProfitValue, predictionProb=bestPredictionProb, stop=stop
        )
        val = val[0]
        print('stop is ' + str(stop) + 'and pandl is ' + str(val))
        if val >= pandl:
            pandl = val
            bestStop = stop

    print("best stop is " + str(bestStop) + "with pandl at " + str(pandl))
            

    result = bestTradeValues(takeProfit=bestTakeProfitValue, stop=bestStop, predictionProb=bestPredictionProb)

    #send trade mechanics to firebase
    firebase.db.child(asset).child('stop').set(bestStop)
    firebase.db.child(asset).child('predictProb').set(bestPredictionProb)
    firebase.db.child(asset).child('takeProfit').set(bestTakeProfitValue)
    firebase.db.child('lastModelRunTime').set(datetime.datetime.now().day)

    #Trade Mechanic Report
    report = 'Best PandL {} || Best Stop: {} || Best Predict Prob:{} || Best Take Profit: {} || CU: {} || IU: {} || CD: {} || ID: {} || Stopped: {} || Take Profit Hit {} || Manual Exit{} ||'.format(result[0], result[1], result[2], result[3], result[4],result[5],result[6],result[7],result[8],result[9],result[10])

    return report    





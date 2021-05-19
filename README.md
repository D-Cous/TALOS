<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="450" height="450">
  </a>

  <h3 align="center">TALOS</h3>

  <p align="center">
TALOS (Technical Analysis Learning Algorithms) is a system of deep learning algorithms to predict and trade crypto currency assets.
<br />
</p>
<br />


<!-- ABOUT THE PROJECT -->

## About The Project

TALOS is a system of deep learning algorithms to predict and trade assets. It runs a model every day at a customizable time to find the best trading patterns, and automatically finds the best stop loss/take profit, sending you morning email report with all of the results. To build the model, a variety of technical indicators were used with a GRU model, however conintuous experimentation is being done to identify the best outcomes. This project was also containerized so that it can be run with minimal set up on any machine. There are improvements that could be made to this program including more efficent data collection for training, better logic for triggering trade logic and utilization of Kubernetes to ensure that if the program crashes, it relaunches.  I have since moved on to other projects but I will update the repo as I make further improvements. 

### Built With

- numpy
- pandas
- tensorflow
- keras
- scikit-learn
- pyrebase
- selenium

<!-- GETTING STARTED -->

## Getting Started

To run TALOS, you will need a Bybit account, Tradingview account, docker installed, as well as to create a "other/creds.py" file containing your Bybit, Tradingview and Gmail credentials. Additionally, you will need to create your own model. It is important to have features for the price open, price high, price low and price close is columns 0,1,2,3 of your pandas dataframe, respectively.
TALOS is set up to run with Firebase as a backend and you will need to enter your credentials into other/firebase.py, including a service account.
Once you have all of the previously mentioned installed and set up, you can customize the trading time period from talosLevers.py, as well as the wager amount and the time that models train everyday.
Running everything is as simple as running talos.py if you have your environment set up with all dependencies. If you have docker installed, you can run `docker-compose up` to start the program on any machine with minimal setup.

The program will send you an email once training is finished with the results from the test set, showing the accuracy, optimal stop loss, optimal take profit and the overall profit and loss.

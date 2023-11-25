# Interactive Brokers data download scripts

This project contains Python scripts for downloading data using the Interactive Brokers TWS API. 

The process of getting the API up and running to collect real time data is described in some detail in [this article](https://www.wrighters.io/how-to-connect-to-interactive-brokers-using-python/). The details of using the API to download historical data are described in [this article](https://www.wrighters.io/how-to-get-historical-market-data-from-interactive-brokers-using-python/).

## Basic setup

1. Download TWS software from [Interactive Brokers](https://www.interactivebrokers.com/). 
1. Create and fund your account
1. Pay for data for the product you want to access
1. Download or upgrade the TWS API from [here](https://interactivebrokers.github.io/). This repo was last tested against 10.19.1.
1. Setup your Python environment (using pyenv, virtualenv, anaconda, whatever...)
1. Install the TWS API in your environment 
1. Install the dependencies

The steps above are mostly manual since you need to do some personalized setup, but the last install step can be done as follows:

```
python -m pip install pip-tools
pip-compile pyproject.toml
pip-sync
```

## Updated Setup

1. Create and fund your account and subscribe to data
2. Download Latest TWS software from [Interactive Brokers](https://www.interactivebrokers.com/). 
   1. File -> Application Settings -> API -> Settings -> General -> Check "Enable ActiveX and Socket Clients" 
3. Download or upgrade the TWS API from [here](https://interactivebrokers.github.io/). This repo was last tested against 10.25.01
4. Install the TWS API in your environment 
   1. unzip twsapi_macunix.1025.01.zip
   2. cd IBJts/source/pythonclient
   3. python setup.py sdist
   4. python setup.py bdist_wheel
   5. pip install dist/ibapi-10.25.1-py3-none-any.whl
5. Setup your Python environment and Install the dependencies
   1. python -m venv venv
   2. source venv/bin/activate
   3. python -m pip install pip-tools
   4. pip-compile pyproject.toml
   5. pip-sync
   6. pip install -r requirements.txt
6. Example Command
   1. `python download_bars.py  --timezone=UTC  TSLA`

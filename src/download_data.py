#!/usr/bin/env python

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import argparse

def get_spy():
    url = 'https://www.slickcharts.com/sp500'
    request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    stats = soup.find('table',class_='table table-hover table-borderless table-sm')
    df =pd.read_html(str(stats))[0]
    df['% Chg'] = df['% Chg'].str.strip('()-%')
    df['% Chg'] = pd.to_numeric(df['% Chg'])
    df['Chg'] = pd.to_numeric(df['Chg'])
    return df

def get_qqq():
    df_list = []

    urls = [
        'https://www.dividendmax.com/market-index-constituents/nasdaq-100',
        'https://www.dividendmax.com/market-index-constituents/nasdaq-100?page=2',
        'https://www.dividendmax.com/market-index-constituents/nasdaq-100?page=3'
    ]

    for url in urls:
        try:
            request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            request.raise_for_status()  # Raise HTTPError for bad requests
            soup = bs(request.text,  "html.parser")
            stats = soup.find('table', class_='mdc-data-table__table')
            temp = pd.read_html(str(stats))[0]
            temp.rename(columns={'Market Cap': 'Market Cap $bn'}, inplace=True)
            df_list.append(temp)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")

    if df_list:
        df = pd.concat(df_list, ignore_index=True)
        return df
    else:
        return None

def get_dia():
    """dataframe of info of all tickers in Dow Jones Industrial Average"""
    url = 'https://www.dogsofthedow.com/dow-jones-industrial-average-companies.htm'
    request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    stats = soup.find('table',class_='tablepress tablepress-id-42 tablepress-responsive')
    pulled_df =pd.read_html(str(stats))[0]
    return pulled_df

def download_dia(resolution, start_date, end_date):
    df = get_dia()
    for symbol in df['Symbol']:
        print(symbol)
        cmd = 'python download_bars.py  --timezone=UTC --size {resolution}  --exchange ARCA --start-date {start_date} --end-date {end_date}'.format(symbol)
        print(cmd)
        exit_code = os.system(cmd)

        # Check the exit code
        if exit_code == 0:
            print("Command executed successfully.")
        else:
            print(f"Command failed with exit code {exit_code} for symbol {symbol}.")
            
def download_qqq(resolution, start_date, end_date):
    df = get_qqq()
    for symbol in df['Symbol']:
        print(symbol)
        cmd = 'python download_bars.py  --timezone=UTC --size {resolution}  --exchange ARCA --start-date {start_date} --end-date {end_date}'.format(symbol)
        print(cmd)
        exit_code = os.system(cmd)

        # Check the exit code
        if exit_code == 0:
            print("Command executed successfully.")
        else:
            print(f"Command failed with exit code {exit_code} for symbol {symbol}.")


def download_spy(resolution, start_date, end_date):
    df = get_spy()
    for symbol in df['Symbol']:
        print(symbol)
        cmd = 'python download_bars.py  --timezone=UTC --size {resolution}  --exchange ARCA --start-date {start_date} --end-date {end_date}'.format(symbol)
        print(cmd)
        exit_code = os.system(cmd)

        # Check the exit code
        if exit_code == 0:
            print("Command executed successfully.")
        else:
            print(f"Command failed with exit code {exit_code} for symbol {symbol}.")

if __file__ == '__main___':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol', type=str, help='Equity symbol', default="")
    parser.add_argument('index', type=str, help='Equity index', default="SPY")
    parser.add_argument('resolution', type=str, help='Data resolution', default="1 day")
    parser.add_argument('start_date', type=str, help='Start date', default="20130101")
    parser.add_argument('end_date', type=str, help='End resoldateution', default="20231231")
        
    # Parse the command-line arguments
    args = parser.parse_args()
    
    if args.symbol != "":
        os.system('python download_bars.py  --timezone=UTC --size {args.symbol}  --exchange ARCA  --start-date {args.start_date} --end-date {args.end_date}')
    elif args.index == "QQQ":
        download_qqq(args.resolution, args.start_date, args.end_date)
    elif args.index == "SPY":
        download_spy(args.resolution, args.start_date, args.end_date)
    elif args.index == "DIA":
        download_dia(args.resolution, args.start_date, args.end_date)

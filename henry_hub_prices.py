# Program for pulling Henry Hub pricing data from EIA website
# Have options to show current price, time range of prices,
# average price over some time, plot data, calculate cost of gas given an MMBTU.
#
# Get data here:
# https://www.eia.gov/opendata/qb.php?sdid=NG.RNGWHHD.D
#
# May also be useful:
# https://www.eia.gov/dnav/ng/ng_pri_fut_s1_d.htm
#
# total gas price = (price per MMBTU) * (MMBTU)
# Will need to work with datetime for using dates (yyyymmdd)

import requests, time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


def page_get(web_page):
    timeout_count = 0
    timeout_check = False
    while not(timeout_check):
        try:
            data_page = requests.get(web_page, timeout = 5)
            timeout_check = True
        except Exception:
            if (timeout_count >= 3):
                return None
            timeout_count += 1
            time.sleep(3)
    return data_page


def price_data_get(web_page, start = None, end = None):
    hh_soup = BeautifulSoup(web_page.text, "lxml")

    # First tr has data label info, will need to skip it!
    price_data_table = hh_soup.find("table", class_ = "basic_table").find_all("tr")

    # Go through historical price data table to get date and price
    price_data_list = []
    for tr_index, tr in enumerate(price_data_table, start = 1):
        if (tr_index == 1):
            pass
        else:
            price_data_point = []
            for td_index, td in enumerate(tr.find_all("td"), start = 1):
                if (td_index == 2):
                    # Might add date formatting here
                    price_data_point.append(int(td.text))
                elif (td_index == 4) and (td.text != "null"):
                    price_data_point.append(float(td.text))
                    price_data_list.append(price_data_point)

    price_data_list.reverse()

    new_data = []
    if (start == None) and (end == None):
        return price_data_list
    elif (start != None) and (end != None):
        for d in price_data_list:
            if (d[0] >= start) and (d[0] <= end):
                new_data.append(d)
        return new_data
    elif (start == None):
        for d in price_data_list:
            if d[0] <= end:
                new_data.append(d)
        return new_data
    elif (end == None):
        for d in price_data_list:
            if d[0] >= start:
                new_data.append(d)
        return new_data


def plot_data(data):
    x_values = [x[0] for x in data]
    y_values = [y[1] for y in data]

    plt.plot(x_values, y_values)
    plt.title("Henry Hub Natural Gas Prices")
    plt.xlabel("Date (yyyymmdd)")
    plt.ylabel("Price (dollar per MMBTU)")

    if (len(data) < 5):
        plt.xticks(x_values)
        plt.yticks(y_values)
    else:
        plt.xticks([x_values[int(len(x_values)*0.2)], x_values[int(len(x_values)*0.4)],
                    x_values[int(len(x_values)*0.6)], x_values[int(len(x_values)*0.8)],
                    x_values[int(len(x_values)-1)]])
        plt.yticks([min(y_values), average_price(y_values), max(y_values)])
        
    plt.ticklabel_format(axis = "x", style = "plain", useOffset = False)
    plt.grid(True)
    #plt.savefig("HH Plot 1")
    plt.show()


def average_price(data):
    price_sum = 0
    if (type(data[0]) == type(list())):
        for price in data:
            price_sum += price[1]
    else:
        for price in data:
            price_sum += price

    return round(price_sum / len(data), 2)


def main():
    henry_page = "https://www.eia.gov/opendata/qb.php?sdid=NG.RNGWHHD.D"
    # list of lists with [date, price] for entries
    user_choice = str()
    while (user_choice != "0"):
        print("Select a number")
        print("1. Plot price data")
        print("2. Get average price")
        print("0. Quit")
        print()

        user_choice = input("Selection: ")
        print()
        if (user_choice == "1"):
            plot_data(price_data_get(page_get(henry_page)))
        elif (user_choice == "2"):
            print("Average price: ", end = "")
            print(average_price(price_data_get(page_get(henry_page))))
            print()
        else:
            pass



henry_page = "https://www.eia.gov/opendata/qb.php?sdid=NG.RNGWHHD.D"
page = page_get(henry_page)
data = price_data_get(page, start = 19990101, end = 20000101)
#data = price_data_get(page)
##for d in data:
##    print(d)

print("avg price:", average_price(data))

plot_data(data)















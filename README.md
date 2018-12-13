# ma_model
moving average trading model

This is a module to do technical stock analysis. User can define their own stock and graph the base graph out from this model. 
This module includes pandas, numpy and matplotlib library. Before using this module, please make sure you have those library installed on your machine.

Download historical stock prices by using below function:
get_data(ticket, startdate, enddate, source='yahoo')
This function will download the historical stock price to your local machine(same folder) as csv file.

Graph histroical stock prices data by using below function:
graph_data(ticker, mvs)
This function do the graphing of a ticker with the moving average (mvs) user defined. 
Sample output:

graph_data('spy', 10, 20, 100)
(https://raw.githubusercontent.com/mablic/ma_model/global/image/.png)

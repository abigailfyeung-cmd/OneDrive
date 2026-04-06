import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib.backends.backend_pdf import PdfPages
from statsmodels.tsa.arima.model import ARIMA 
from statsmodels.tsa.statespace.sarimax import SARIMAX 
#0 import
df = pd.read_csv("C:/Users/abiga/OneDrive/monthly-milk-production.csv")
df.columns = ['Month','Milk in pounds per cow']
print(df.head())

df['Month'] = pd.to_datetime(df['Month'])
print(df.head())
#1 data print
df.set_index('Month', inplace=True)
print(df.head())

#2 rolling average print
timeseries = df['Milk in pounds per cow']
timeseries.rolling(12).mean().plot(label='12 Month Rolling Mean')

#3 decomposition print
decomposition = seasonal_decompose(df['Milk in pounds per cow'], period=12)

#4 model generation and print
# ARIMA - Auto Regressive Integrated Moving Average
amodel = ARIMA(df['Milk in pounds per cow'], order = (10, 1, 5))
#try 5, 1, 0
afit = amodel.fit()
aforecast = afit.forecast(steps=12)

with PdfPages("les7_plots.pdf") as pdf:
#1
     df.plot()
     plt.title("Monthly milk production data")
     pdf.savefig()
     plt.close()
    

#2
     timeseries.plot()
     plt.title("Milk production with seasonality removed")
     pdf.savefig()
     plt.close()

#3
     decomposition.plot()
     plt.title("Milk production decomposition")
     pdf.savefig()
     plt.close()

#4
     df['Milk in pounds per cow'].plot(label = 'Data')
     aforecast.plot(label = 'ARIMA Prediction', color = 'red')
     plt.legend()
     pdf.savefig()
     plt.close()
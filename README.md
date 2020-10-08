## Project Luther

The purpose of this project is to build and compare the performance of 3 different models (the purpose is NOT: to build an ACCURATE model).  
This is the [Jupyter notebook](lutherMain.ipynb).   
Here is a [powerpoint format](jcosme-project2.pptx) of the presentation, and here is a [pdf format](jcosme-project2.pdf) of the presentation.  

### The Data
We scraped S&P 500 components, and historic component changes, from this [wikipedia page](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).  
Then we used the Yahoo Finance pandas API to get historic price data, for all components.  
Finally, we scraped Key Statistics for all component, from the component's Yahoo Finance page.  
Here is an example for [Apple stock](https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL) Key Statistics.  
Here is the [python script](scrapeAndGetData.py) used to gather the data.

### The Models
The models attempt to forecast tomorrow's return (% price change), given today's information.  
We build the following models:
+ *Simple Model:* An Auto-Regressive(1) model, that uses only today's returns to predict tomorrow's return.  
+ *Complex Model:* A regression model which uses available Key Statistics, in addition to today's return, to make a prediction.
+ *Neural Network Model:* A Neural Network implimentation of the Complex Model.  

### Results
There is not strong evidence to suggest that the out-of-sample forecast performance of the Simple and Complex models are different.  
Because the Complex model gives no improvement over the Simple model (in fact, performed slightly worse), it would be better to use the simple model.  
A one-way ANOVA of the errors of the 3 models, suggests that the performance of the Neural Network is indeed different from the other two models. Since it had the best performance, it would be best to use this model over the others. 
But none should actually be used since they are all terrible.  


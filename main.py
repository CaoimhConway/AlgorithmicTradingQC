# Use 5 ETFs (SPY - US stocks, EFA - foreign stocks, IEF - bonds, VNQ - REITs, GSG - commodities).
# Pick 3 ETFs with strongest 12 month momentum into your portfolio and weight them equally. 
# Hold for 1 month and then rebalance.

import pandas as pd
from datetime import datetime

class AssetClassMomentumAlgorithm(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2000, 1, 1)  
        self.SetEndDate(datetime.now())  
        self.SetCash(100000)
        
        
        self.data = {}
        period = 12*21
        self.symbols = ["SPY", "EFA", "IEF", "VNQ", "GSG"]
        
        self.SetWarmUp(period)
        
        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Daily)
            self.data[symbol] = self.MOM(symbol, period, Resolution.Daily)
         
        self.Schedule.On(self.DateRules.MonthStart("SPY"), self.TimeRules.AfterMarketOpen("SPY"), self.Rebalance)
            
    def OnData(self, data):
        pass

    def Rebalance(self):
        if self.IsWarmingUp: return
        top3 = pd.Series(self.data).sort_values(ascending = False)[:3]
        for kvp in self.Portfolio:
            security_hold = kvp.Value
           
            if security_hold.Invested and (security_hold.Symbol.Value not in top3.index):
                self.Liquidate(security_hold.Symbol)
        
        added_symbols = []        
        for symbol in top3.index:
            if not self.Portfolio[symbol].Invested:
                added_symbols.append(symbol)
        for added in added_symbols:
            self.SetHoldings(added, 1/len(added_symbols))

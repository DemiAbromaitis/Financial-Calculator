# -*- coding: utf-8 -*-
"""
Defines Bond and Portfolio Classes, equations specific to analysis of bonds.
@author: DemiAbromaitis
"""


import FS_MAIN as FS
import numpy as np


#-----------------------------------------------------
#PORTFOLIO OBJECT CLASS:
    #contains list of asset class data inherently
#-----------------------------------------------------
class Portfolio(object):
    def __init__(self, 
                 assetList, 
                 returnCFsList=None):
        self.data = {
            'assetList' : assetList,
            'returnCFs' : returnCFsList,
            
            }

    #DESIRED CF RETURN TIMELINE FOR PORTFOLIO 
    def AddReturnCFs(self, returnCFList):
        self.data['returnCFList']=returnCFList
        print("portfolio data updated")

#-----------------------------------------------------
#!!! BOND OBJECT CLASS
    #contains basic properties of bond security inherently
#-----------------------------------------------------       

class Bond(object):
    def __init__(self, 
                 faceValue, 
                 maturity, 
                 coupon, 
                 couponRate, 
                 price, 
                 compPeriods=1, 
                 intRate=0, 
                 CF_growthRate=0, 
                 CF_growthPeriods=None, 
                 ArrowDebreu=None):
        self.data = {
            'CF_T' : faceValue, #final payout for bonds
            'Time' : maturity, #maturity, years
            'CF_t1': coupon, #first cash flow,
            'CF_rate' : couponRate, #ratio to CF_T
            'priceT0' : price, #initial price
            'k' : compPeriods, #per year
            'intRate' : intRate,
            'CF_growthRate' : CF_growthRate,
            'CF_growthPeriods' : CF_growthPeriods,
            'ArrowDebreu' : ArrowDebreu,
            #'time_k' : (maturity*compPeriods),
             }
        
#---------------------------------------------------------        
#!!! BOND SPECIFIC FUNCTIONS
#---------------------------------------------------------




#DISCOUNT BONDS
    #SOLVE PRICE market using spot rate for given time 
    def DB_CurrentPrice (time, interestRate):
        ''' 
        solves Bt or current price of discount bond
        input: spot rate t=0, time
        '''
        Bt= 1/((1+interestRate)**time)
        print("Current Price of discount bond: $")
        return Bt        
    #SOLVE SPOT RATE at specified time
    def DB_SpotRate(self, time):
        
        ''' 
        solves for spot rate at time=0
        given discount bond price (Bt) and time to maturity
        returns % as float
        '''
        interestRate = (1 / self.data['price']**(1/self.data['time']))-1
        print("Spot rate T=0, given bond price: ")
        return interestRate  
    
#CF LIST GEN CLASS SPECIFIC
def CFListGen (self):
    print("Bond.CFListGen Called")
    #assignments from dictionary
    CF_T = self.data['CF_T']
    Time = self.data['Time']
    CF_t1 = self.data['CF_t1']
    CF_rate = self.data['CF_rate']
    CF_growthRate = None
    CF_growthPeriods = None
    k = self.data['k']
    #generate CF list 
    self.data['CFListY1'] = FS.CFListGen(CF_T, Time,
                     CF_t1, CF_rate, 
                     CF_growthRate, 
                     CF_growthPeriods, 
                     k)
    #stores CF List to bond
#PVCF LIST GEN - CLASS SPECIFIC
def PVCFListGen(self):
    print("Bond.PVCFListGen Called")
    self.data['PVCFList']= FS.PVCFListGen(self)
    
#CURRENT MARKET PRICE OF ASSET FROM CF AND YIELD
def Price_CFandYield(self, YTM):
    ''' 
    RETURN : 
        bond price from YTM
    PARAMETERS : 
        self, one instance of class Bond
        YTM, float, yield to maturity
    '''
    #if Cash Flow List does not exist (Y1->maturity)
    if 'CFListY1' not in self.data:
        #generate CF list 
        Bond.CFListGen(self)
    
    Price = 0
    for t in range (0, len(self.data['CFListY1'])):
        Price += self.data['CFListY1'][t] / ((1+YTM)**(t+1))
    print("Present value/Price Calculated from CFs and YTM: $", str(Price))
    #return Price
    
#CALCULATE COUPON BOND PRICE FROM LIST OF DISCOUNT BOND PRICES
def CBond_Price_DBPriceList (self, DBondPriceList):
    ''' 
    uses Bt trend list, coupon and principal payments, maturity
    solves current price of coupon bond ($)
    '''
    B = 0 #define bond price
    for t in range(0, self.data['Time']): #because t1 is index0 exclude time
        B += (self.data['CF_t1'] * DBondPriceList[t])
    B += (self.data['CF_T'] * DBondPriceList[self.time-1]) #assigns accurate index
    print("Current Coupon Bond Price: ($)", str(B))
    return B    

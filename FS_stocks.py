# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:00:01 2023
Defines Stock class of assets, defines functions specific to stock value and analysis.

@author: Demir
"""
import FS_MAIN as FS

class Stock(object):
    def __init__(self, 
                 Price_T,   
                 endYear,     
                 dividend_t1,
                 price_T0,
                 compPeriods = 1,
                 intRate = 0,
                 Div_growthRate = 0,
                 Div_growthPeriods = None, 
                 ArrowDebreu = None):
        self.data = {
            'CF_T' : Price_T,       #final payout for sale of share
            'Time' : endYear,       #time at which to sell
            'CF_t1': dividend_t1,   #first cash flow,
            'priceT0' : price_T0,   #initial price
            'k' : compPeriods,      #per year
            'intRate' : intRate,    #discount rate, market int rate
            'CF_growthRate' : Div_growthRate,   #None, int/float, or list of
            'CF_growthPeriods' : Div_growthPeriods, #
            'ArrowDebreu' : ArrowDebreu,
            'CF_rate' : None
            #'time_k' : (maturity*compPeriods),
             }


#---------------------------------------------------------
#!!! VALUE ASSIGNMENT FOR FUNCTIONS: 
#   prioritizes function input data over asset class stored data


def f_EPSratio(asset, EPSratio, time=1):
    if asset != None:
        #DEFINE FROM ASSET OR EXCEPTION
        if 'EPSratio' not in asset.data.keys() and type(EPSratio) not in (int,float):
            #print("EPSratio not given for given security.")
            EPSratio = None
        elif 'EPSratio' in asset.data.keys() and EPSratio not in (int, float):
           #print("EPSratio found")
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['EPSratio']) in (int, float):
                #print("EPS Stored as local variable")
                EPSratio = asset.data['EPSratio']
                #print("EPSt1 Ratio: ", str(EPSratio))
            #FILL FOR NONCONSTANT GROWTH
            #elif type(asset.data['EPSratio']) == list:
                #EPSratio = asset.data['EPSratio'][time-1]
            else:
                print("security data for EPSratio incorrect type.")
                EPSratio =  None
    return EPSratio
def f_DPSratio(asset, DPSratio, time=1):
    if asset != None:
        #DEFINE FROM ASSET OR EXCEPTION
        if 'DPSratio' not in asset.data.keys() and type(DPSratio) not in (int,float):
            #print("DPSratio not given for given security.")
            DPSratio = None
        elif 'DPSratio' in asset.data.keys() and DPSratio not in (int, float):
           #print("DPSratio found")
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['DPSratio']) in (int, float):
                #print("EPS Stored as local variable")
                DPSratio = asset.data['DPSratio']
                #print("DPSratio Ratio: ", str(DPSratio))
            #FILL FOR NONCONSTANT GROWTH
            #elif type(asset.data['DPSratio']) == list:
                #DPSratio = asset.data['DPSratio'][time-1]
            else:
                print("security data for DPSratio incorrect type.")
                DPSratio =  None
    return DPSratio
def f_GrowthRate(asset, growthRate, time=1):      
    if asset!= None:
        #print("asset detected")
        #DEFINE FROM ASSET OR EXCEPTION
        if 'CF_growthRate' not in asset.data.keys() and growthRate == None:
            #print("CF_growthRate not given for given security. ")
            growthRate = None
        elif 'CF_growthRate' in asset.data.keys() and growthRate == None:
            #print('CF_growthRate found')
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['CF_growthRate']) in (int, float):
                growthRate = asset.data['CF_growthRate']
                #print('CF_growthRate stored', str(growthRate))
            elif type(asset.data['CF_growthRate']) == list:
                growthRate = asset.data['CF_growthRate'][time-1]
            #FILL FOR NONCONSTANT GROWTH
            
            else:
                #print("security data for CF_growthRate incorrect type. Stored None")
                growthRate = None
    return growthRate
def f_invReturnRate(asset, invReturnRate, time=1):      
    if asset!= None:
        #print("asset detected")
        #DEFINE FROM ASSET OR EXCEPTION
        if 'invReturnRate' not in asset.data.keys() and invReturnRate == None:
            #print("invReturnRate not given for given security. ")
            invReturnRate = None
        elif 'invReturnRate' in asset.data.keys() and invReturnRate == None:
            #print('invReturnRate found')
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['invReturnRate']) in (int, float):
                invReturnRate = asset.data['invReturnRate']
                #print('invReturnRate stored', str(invReturnRate))
            elif type(asset.data['invReturnRate']) == list:
                invReturnRate = asset.data['invReturnRate'][time-1]
            #FILL FOR NONCONSTANT GROWTH
            
            else:
                #print("security data for invReturnRate incorrect type. Stored None")
                invReturnRate = None
    return invReturnRate      
def f_PAYOUTratio(asset, PAYOUTratio, time=1):      
    if asset!= None:
        #print("asset detected for payout ratio")
        #DEFINE FROM ASSET OR EXCEPTION
        if 'PAYOUTratio' not in asset.data.keys() and PAYOUTratio == None:
            #print("PAYOUTratio not given for given security. ")
            PAYOUTratio = None
            
        elif 'PAYOUTratio' in asset.data.keys() and PAYOUTratio == None:
            #print('PAYOUTratio found')
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['PAYOUTratio']) in (int, float):
                PAYOUTratio = asset.data['PAYOUTratio']
                #print('PAYOUTratio stored', str(PAYOUTratio))
            elif type(asset.data['PAYOUTratio']) == list:
                PAYOUTratio = asset.data['PAYOUTratio'][time-1]
            #FILL FOR NONCONSTANT GROWTH            
            else:
                #print("security data for PAYOUTratio incorrect type.")
                PAYOUTratio = None
    return PAYOUTratio
def f_bookValueY0(asset, bookValueY0, time=1):
    if asset!= None:
        #print("asset detected for bookValueY0")
        #DEFINE FROM ASSET OR EXCEPTION
        if 'bookValueY0' not in asset.data.keys() and bookValueY0 == None:
            #print("bookValueY0 not given for given security. ")
            bookValueY0 = None
            
        elif 'bookValueY0' in asset.data.keys() and bookValueY0 == None:
            #print('bookValueY0 found')
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['bookValueY0']) in (int, float):
                bookValueY0 = asset.data['bookValueY0']
                #print('bookValueY0 stored', str(bookValueY0))
            elif type(asset.data['bookValueY0']) == list:
                if time != None:
                    bookValueY0 = asset.data['bookValueY0'][time-1]
                else:
                    bookValueY0 = asset.data['bookValueY0']
            #FILL FOR NONCONSTANT GROWTH            
            else:
                #print("security data for bookValueY0 incorrect type.")
                bookValueY0 = None
    return bookValueY0
def f_Earnings(asset, earnings, time=1):
    if asset!= None:
        #print("asset detected for earnings")
        #DEFINE FROM ASSET OR EXCEPTION
        if 'earnings' not in asset.data.keys() and earnings == None:
            #print("earnings not given for given security. ")
            earnings = None
            
        elif 'earnings' in asset.data.keys() and earnings == None:
            #print('earnings found')
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['earnings']) in (int, float):
                earnings = asset.data['earnings']
                #print('earnings stored', str(earnings))
            elif type(asset.data['earnings']) == list:
                if time != None:
                    earnings = asset.data['earnings'][time-1]
                if time == None:
                    earnings = asset.data['earnings']
            #FILL FOR NONCONSTANT GROWTH            
            else:
                #print("security data for earnings incorrect type.")
                earnings = None
    return earnings
def f_FCFListY1(asset, FCFListY1, time=1):
    if asset!= None:
        #print("asset detected for FCFListY1")
        #DEFINE FROM ASSET OR EXCEPTION
        if 'FCFListY1' not in asset.data.keys() and FCFListY1 == None:
            #print("FCFListY1 not given for given security. ")
            FCFListY1 = None         
        elif 'FCFListY1' in asset.data.keys() and FCFListY1 == None:
            #print('FCFListY1 found')
            if type(asset.data['FCFListY1']) == list:
                if type(time) in (int, float):
                    FCFListY1 = asset.data['FCFListY1'][time-1]
                else:
                    FCFListY1 = asset.data['FCFListY1']
            #FILL FOR NONCONSTANT GROWTH            
            else:
                #print("security data for FCFListY1 incorrect type.")
                FCFListY1 = None
    return FCFListY1
               


#---------------------------------------------------------
#!!! CF LIST GEN CLASS SPECIFIC
def CFListGen (self):
    """
    Description:
    -------
    Class specific data assignments for FS_MAIN CFListGen Fucntion

    Returns
    -------
    None. Stores CFListY1 to self.data['CFListY1']
    
    """
    
    print("Stock.CFListGen Called")
    #assignments from dictionary
    CF_T = self.data['CF_T']
    Time = self.data['Time']
    CF_t1 = self.data['CF_t1']
    CF_rate = None
    CF_growthRate = self.data['CF_growthRate']
    CF_growthPeriods = self.data['CF_growthPeriods']
    k = self.data['k']
    #generate CF list 
    self.data['CFListY1'] = FS.CFListGen(CF_T, Time,
            CF_t1, CF_rate, CF_growthRate, 
            CF_growthPeriods, k)
    #stores CF List to stock

        
#---------------------------------------------------------
#!!! REINVESTMENT & GROWTH OF STOCKS: 
#   EARNINGS, DIVIDENDS, PAYOUT, PLOWBACK, REINVESTMENT SOLVERS

        
#DPS, EPS, PAYOUT, PLOWBACK, REINVESTMENT CALCULATORS:
def PAYOUTratio_NoDebt (asset, DPSratio, EPSratio, time=1):
    '''
    Parameters
    ----------
    DPSratio : FLOAT. dollars per share
    EPSratio : FLOAT. dollars per share

    Returns
    -------
    p : FLOAT. payout ratio (no unit)
    '''
    print("FSs.PAYOUTraio_NoDebt Called")
    #INITIALIZE VARIABLES WITH ASSET OR INPUTS
    EPSratio = f_EPSratio(asset, EPSratio, time)
    DPSratio = f_DPSratio(asset, DPSratio, time)
    #CALCULATE
    payout = DPSratio / EPSratio
    print("payoutRatio for asset: ", str(payout))
    return payout
#CALCULATE DPSratio FROM EPS AND PAYOUT RATIOS
def DPSratio_EPSandPayout (asset, EPSratio, PAYOUTratio, time=1):
    """
    Parameters
    ----------
    asset : security class instance or none
    
    PAYOUTratio : float, no units
        paid dividends $ : retained earnings $.
        
    EPSratio : FLOAT, dollar
        earnings $ per share.

    Returns
    -------
    DPSratio : float, dollar
        dividends per share.

    """
    #IF ASSET DEFINED
    PAYOUTratio = f_PAYOUTratio(asset, PAYOUTratio, time)
    EPSratio = f_EPSratio(asset, EPSratio, time)
        
    #IF ASSET UNDEFINED, USE FORMULA INSTANCE ENTRIES:    
    DPSratio = PAYOUTratio * EPSratio
    print("DPSratio calculated : $ ", str(DPSratio))
    return DPSratio
#CALCULATE INVESTMENT FROM EPS AND PAYOUT OF THAT YEAR
def InvestmentT1_EPSPAYOUT (asset, EPSratio, PAYOUTratio, time=1):
    """
    

    Parameters
    ----------
    asset : security class instance or none
    EPSt1 : FLOAT, NONE. dollars per share
    payoutRatio : FLOAT OR NONE. ratio of payout to earnings

    Returns
    -------
    InvestmentT1 : FLOAT, dollars. investment

    """
    EPSratio = f_EPSratio(asset, EPSratio)
    PAYOUTratio = f_PAYOUTratio(asset, PAYOUTratio, time)
            
    #IF ASSET IS NONE, USE FORMULA INSTANCE DATA
    InvestmentT1 = (1-PAYOUTratio)*EPSratio  
    print("Reinvested Earnings for year calculated: $ ", str(InvestmentT1))
    return InvestmentT1
#INFER NEXT EPS DATA FROM SPECIFIED YEAR INVESTMENT AND EPS
def EPS_t2 (asset, EPSratio, Invest_T1, invReturnRate, time=1):
    """
    

    Parameters
    ----------
    asset : TYPE
        DESCRIPTION.
    EPSratio : TYPE
        DESCRIPTION.
    Invest_t1 : TYPE
        DESCRIPTION.
    invReturnRate : TYPE
        DESCRIPTION.

    Returns
    -------
    EPSt2 : TYPE
        DESCRIPTION.

    """
    EPSratio = f_EPSratio(asset, EPSratio, time)
    invReturnRate = f_invReturnRate(asset, invReturnRate, time)
    PAYOUTratio = f_PAYOUTratio
    
      
    #DEFINE FROM ASSET OR EXCEPTION
    if asset!= None:
        if 'Invest_T1' not in asset.data.keys() and Invest_T1 == None:
            print("Invest_T1 not given for given security. EPSratioT2 not calculated.")
            return None
        elif 'Invest_T1' in asset.data.keys() and Invest_T1 == None:
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['Invest_T1']) in (int, float):
                Invest_T1 = asset.data['Invest_T1']
            
            #FILL FOR NONCONSTANT GROWTH
            else:
                print("security data for Invest_T1 incorrect type. EPSratioT2 not calculated. \n\n")
        else: 
            Invest_T1 = InvestmentT1_EPSPAYOUT(asset, EPSratio, PAYOUTratio)

    
    EPSratioT2 = EPSratio + (Invest_T1 * invReturnRate)
    print("the next years EPS ratio calculated from current EPS, investment, returnRate: ", str(EPSratioT2))
    
    return EPSratioT2
#SOLVE GROWTH RATE FOR YEAR T, FROM EPS T & T+1
def GrowthRate_EPS(asset, EPSt1, EPSt2, year=1):
    ''' 
    calculates growth rate of earnings given EPS for years 1 and 2
    assumes investment and return are linear
    '''
    print("GrowthRate T1 from EPS T1 and T2")
    
    gr = EPSt2/EPSt1 - 1
    print("Growth rate of EARNINGS from YEAR T to T+1: ", str(gr))
    return gr
#CALC PAYOUT AND PLOWBACK RATIO FROM GROWTH and INV RETURN RATE
def PAYOUTPLOWBACKratio_CGInvest (asset, growthRate, invReturnRate, time=1):
    """
    

    Parameters
    ----------
    asset : class instance or none.
    growthRate : float or none.
    invReturnRate : float or none.

    Returns
    -------
    PAYOUTratio.

    """
    print("FSs.PAYOUTratio_CGInvest Called")
    growthRate = f_GrowthRate(asset, growthRate, time)
    invReturnRate = f_invReturnRate(asset, invReturnRate, time)
    print("growth rate = ", str(growthRate))        
    #if asset is none, proceed with formula instance data:    
    b_plowback = ((1+growthRate)-1)/invReturnRate
    p_payout= 1-b_plowback
    print("Payout, Plowback Ratios: ", str([p_payout, b_plowback]))
    return [p_payout, b_plowback]


#!!!  REINVESTMENT & GROWTH:
#   PRESENT VALUE, NPV, PRICE OF STOCKS

#CALCULATE NPV (NET PRESENT VALUE) OF GIVEN YEAR
def NPVt1_inv (asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, time=1):
    """
    

    Parameters
    ----------
    asset : INSTANCE OF CLASS OR NONE
        none if not pulling from any asset.data{}
        
    EPSratio : $ , FLOAT or NONE 
        earnings per share
        
    discRate : FLOAT or NONE
        market interest rate to discount for PVs.
    growthRate : INT, FLOAT or NONE
        ratio, growth rate of earnings
    invReturnRate : INT, FLOAT, NONE
        $ , return on investment from earnings.
    PAYOUTratio : ratio
        ratio, what % of earnings paid out in dividends.

    Returns
    -------
    NPVT1 : FLOAT
        net present value of investment .

    """
    
    """
    calculate NPV of given year (default 1), with given stock data
    assumes linear or no growth of investment/earnings
    
    """
    print("FSs.NPVt1_inv called")
    EPSratio = f_EPSratio(asset, EPSratio, time)
    growthRate = f_GrowthRate(asset, growthRate, time)
    PAYOUTratio = f_PAYOUTratio(asset, PAYOUTratio, time)
    invReturnRate = f_invReturnRate(asset, invReturnRate, time)
    if PAYOUTratio == None:
        p, b = PAYOUTPLOWBACKratio_CGInvest(growthRate, invReturnRate)
    else:
        p = PAYOUTratio
    InvestmentT1 = InvestmentT1_EPSPAYOUT(None, EPSratio, p)
    NPVT1= -InvestmentT1 + ( (invReturnRate*InvestmentT1)/discRate )
    print("\n\nNPV for T1 is calculated : $", str(NPVT1))
    return NPVT1
#STOCK PRICE FROM FROM EPS
def Price_EPS (asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, year=1):
    '''
    
    assume earnings growth is constant increasing perpetuity
    
    Parameters
    ----------
    EPSt1 : FLOAT. earnings per share ratio
    discRate : FLOAT. interest or discount rate
    growthRate : FLOAT, dollar. increase in earnings per year
    invReturn : FLOAT, ratio of return for $1 invested
    payoutRatio : FlOAT, ratio of payouts to earnings,
        make 0 if unknown
    Returns
    -------
    P0 : current price of stock

    '''
    print("FSs.Price_EPS function called.\n")
    #if no reinvestment and no increase in earnings:
   
    EPSratio = f_EPSratio(asset, EPSratio, year)
    PAYOUTratio = f_PAYOUTratio(asset, PAYOUTratio, year)
    growthRate = f_GrowthRate(asset, growthRate, year)
    invReturnRate = f_invReturnRate(asset, invReturnRate, year)
    
    
    if growthRate == 0:
        print("growth rate 0 found")
        DPSt1 = EPSratio
        print("DPSt1: ", str(DPSt1))
        P0 = DPSt1/discRate
        print("Price from EPS with zero growth: $", str(P0))
        return P0
    #reinvestment, payout ratio known, growth of payout unknown
    elif growthRate == None and PAYOUTratio != None:
        Invest_T1 = InvestmentT1_EPSPAYOUT(None, EPSratio, PAYOUTratio)
        DPSt1 = DPSratio_EPSandPayout(None, EPSratio, PAYOUTratio)
        EPSt2 = EPS_t2(None, EPSratio, Invest_T1, invReturnRate)
        gr = GrowthRate_EPS(None, EPSratio, EPSt2, year)
        print("\nInvestment Y1 = $ ", str(Invest_T1))
        print("\nDPS year", str(year), "= $ :",  str(DPSt1))
        print("\nEPS year ", str(year+1), "= $ :", str(EPSt2))
        print("\nGrowth Rate calculated = ", str(gr))
        #print("growth rate of earnings : ", str(growthRate))
        #P0 = FS.PV_Perpetuity(DPSt1, discRate, growthRate)
        #return P0
    #if growthRate known and payoutRatio not known
    elif growthRate > 0 or growthRate <0:
        print("\nNonzero growth detected")
        if PAYOUTratio == None:
            #compute plowback without p
            p_payout, b_PLOWBACK = PAYOUTPLOWBACKratio_CGInvest(asset, growthRate, invReturnRate)
            print("\nPlowback ratio = b = ", str(b_PLOWBACK))
        else:
            p_payout = PAYOUTratio
        DPSt1 = DPSratio_EPSandPayout(None, EPSratio, p_payout)
        print ("\nDPSt1 calculated: $", str(DPSt1))
        gr = growthRate
        #use FS perpetuity because Div
    P0 = FS.PV_Perpetuity(DPSt1, discRate, gr)
    print ("\nPrice at year", str(year),"= $: ", str(P0))
    return P0
#CALCULATE PVGO - PRESENT VALUE OF GROWTH OPPORTUNITY 
def PVGO_EPS(asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio=0):  
    """
    

    Parameters
    ----------
    asset : class or none
        instance of security class data dictionary.
    EPSratio : int, float, none
        $, earnings per share.
    discRate : int, float, #FILL FOR LIST
        market interest rate for discounting to pv.
    growthRate : int, float, list of, none.
        growth in earnings.
    invReturnRate : int, float, list, none
        Return on re - invested earnings.
    PAYOUTratio : float, optional
        ratio of earnings paid to shareholders. The default is 0.

    Returns
    -------
    PVGO : float, int
        $, present value of current growth opportunity.

    """
    EPSratio = f_EPSratio(asset, EPSratio)
    growthRate = f_GrowthRate(asset, growthRate)
    invReturnRate = f_invReturnRate(asset, invReturnRate)
    PAYOUTratio = f_PAYOUTratio(asset, PAYOUTratio)
        
    print("\n\nWITHOUT GROWTH: ")
    P0_nogrowth = Price_EPS(asset, EPSratio, discRate, 0, invReturnRate, PAYOUTratio)
    print("$ ", str(P0_nogrowth))
    
    
    print("\n\nWITH  GROWTH: ")
    P0_growth = Price_EPS(asset, None, discRate, None, None, None)
    print("$ ", str(P0_growth))
    
    
    PVGO= P0_growth - P0_nogrowth
    
    print("\n\nWITH  GROWTH: $", str(P0_growth))
    print("\n\nWITHOUT  GROWTH: $", str(P0_nogrowth))
    print("\n\nThe PV of Growth Opportunity of Stock: $ \n (growth vs no growth P0)", str(PVGO))
    return PVGO
def PVGO_NPV1_CG(asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, time=1):
    ''' 
    calculates present value of growth opportunity from
    given stock data. assumes linear or 0 earnings growth
    '''
    EPSratio = f_EPSratio(asset, EPSratio, time)
    growthRate = f_GrowthRate(asset, growthRate, time)
    invReturnRate = f_invReturnRate(asset, invReturnRate, time)
    PAYOUTratio = f_PAYOUTratio(asset, PAYOUTratio)
    
    NPVt1 = NPVt1_inv(asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio)
    print('\n\n NPV calculated: ', str(NPVt1))
    Invest_t1 = InvestmentT1_EPSPAYOUT(None, EPSratio, PAYOUTratio, time)
    EPSt2 = EPS_t2(None, EPSratio, Invest_t1, invReturnRate, time)
    if growthRate == None: 
        g = GrowthRate_EPS(None, EPSratio, EPSt2, time)
    else:
        g= growthRate
    PVGO = NPVt1/(discRate-g)
    print("Present value of growth opportunity (at time", str(time), " = $:", str(PVGO))
    return PVGO
def PEratio_EPSandPVGO (asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, time=1):  
    """
    

    Parameters
    ----------
    asset : class instance or none.
        if security class instance data is referenced or manual input of data
    EPSratio : float, int, list, none.
        earnings per share, $
    discRate : float or int
        interest rate or discount rate for PV calculations.
    growthRate : float, int, list, none.
        growth rate of earnings.
    invReturnRate : float, int, list, none
        return on invested earnings.
    PAYOUTratio : float, int, list, none.
        ratio of earnings paid out in dividends.
    time : int, optional
        time to maturity, or target year of calculation. The default is 1.

    Returns
    -------
    PEratio : float or int.
        coefficient of security price to earnings for given year t.

    """
    EPSratio = f_EPSratio(asset, EPSratio, time)
    PVGO = PVGO_NPV1_CG(asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, time=1)
    if PVGO == 0:
        PEratio = 1/discRate
    elif PVGO > 0:
        PEratio = (1/discRate)+ (PVGO/EPSratio)
    else:
        PEratio=None
        print("error in data check PVGO calculation")
    print("\nP/E Ratio from EPSt1, NPV:  ", str(PEratio), '\n')
    return PEratio
def PVt1_EPSt2andPE (asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, time=1):  
    """
    
    Parameters
    ----------
    asset : class instance or none.
        if security class instance data is referenced or manual input of data
    EPSratio : float, int, list, none.
        earnings per share, $
    discRate : float or int
        interest rate or discount rate for PV calculations.
    growthRate : float, int, list, none.
        growth rate of earnings.
    invReturnRate : float, int, list, none
        return on invested earnings.
    PAYOUTratio : float, int, list, none.
        ratio of earnings paid out in dividends.
    time : int, optional
        time to maturity, or target year of calculation. The default is 1.

    Returns
    -------
    PV_time : int, float.
        $, present value (price) of stock from EPS and PE.

    """
    
    EPSratio = f_EPSratio(asset, EPSratio, time)
    PVGO = PVGO_NPV1_CG(asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, time=1)
    if PVGO == 0:
        PEratio = 1/discRate
    elif PVGO > 0:
        PEratio = (1/discRate)+ (PVGO/EPSratio)
    else:
        PEratio=None
        print("error in data check PVGO calculation")
    print("P/E Ratio from EPSt1, NPV:  ", str(PEratio))
    return PEratio
#PRESENT VALUE 

    
    

#---------------------------------------------------------
# !!! REINVESTMENT GENERATOR FUNCTIONS: from retained earnings

#REINVESTMENT CF LIST 
def ReInvestListGen (asset, EPSratio, discRate, growthRate, invReturnRate, PAYOUTratio, endYear, growthPeriods=None):
    print("FSs.ReInvestListGen called")
    if growthPeriods == None and endYear == None:
        if asset!= None:
            if 'CF_growthPeriods' in asset.data.keys():
                if type(asset.data['CF_growthPeriods']) == list: 
                    endYear = sum(asset.data['CF_growthPeriods'])
                elif type(asset.data['CF_growthPeriods']) in (int, float):
                    endYear = asset.data['CF_growthPeriods']
                else:
                    print("CF_growthPeriods data for asset not correct. ReInvestCFList not generated")
                    return None 
                
    if asset != None: 
        #DEFINE FROM ASSET OR EXCEPTION
        if 'EPSratio' not in asset.data.keys() and EPSratio == None:
            print("EPSratio not given for given security. ReInvestCFList not calculated.")
            return None
        elif 'EPSratio' in asset.data.keys() and EPSratio == None:
            
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['EPSratio']) in (int, float):
                EPSratio = asset.data['EPSratio']
            
            #FILL FOR NONCONSTANT GROWTH
            else:
                print("security data for EPSratio incorrect type. ReInvestCFList not calculated. \n\n")
                return None
        
        #DEFINE FROM ASSET OR EXCEPTION
        if 'CF_growthRate' not in asset.data.keys() and growthRate == None:
            print("growthRate not given for given security. ReInvestCFList not calculated.")
            return None
        elif 'CF_growthRate' in asset.data.keys() and growthRate == None:
            
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['CF_growthRate']) in (int, float):
                growthRate = asset.data['CF_growthRate']
            
            #FILL FOR NONCONSTANT GROWTH
            else:
                print("security data for growthRate incorrect type. ReInvestCFList not calculated. \n\n")
                return None
        
        #DEFINE FROM ASSET OR EXCEPTION
        if 'invReturnRate' not in asset.data.keys() and invReturnRate == None:
            print("invReturnRate not given for given security. ReInvestCFList not calculated.")
            return None
        elif 'invReturnRate' in asset.data.keys() and invReturnRate == None:
            
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['invReturnRate']) in (int, float):
                invReturnRate = asset.data['invReturnRate']
            
            #FILL FOR NONCONSTANT GROWTH
            else:
                print("security data for invReturnRate incorrect type. ReInvestCFList not calculated. \n\n")
                return None
        #DEFINE FROM ASSET OR EXCEPTION
        if 'PAYOUTratio' not in asset.data.keys():
            if PAYOUTratio in (0, None):
                p, b = PAYOUTPLOWBACKratio_CGInvest(asset, growthRate, invReturnRate)
            else:
                p = PAYOUTratio
        elif 'PAYOUTratio' in asset.data.keys() and PAYOUTratio == None:
            
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['PAYOUTratio']) in (int, float):
                PAYOUTratio = asset.data['PAYOUTratio']
            
            #FILL FOR NONCONSTANT GROWTH
            else:
                print("security data for PAYOUTratio incorrect type. ReInvestCFList not calculated. \n\n")
                return None

    if PAYOUTratio in (0, None) and growthRate in (0, None):
        p, b = PAYOUTPLOWBACKratio_CGInvest(asset, growthRate, invReturnRate)
    else:
        p = PAYOUTratio
             
    invCFListY1 = []
    print('payout ratio found:', str(p), "\n")
    for t in range (0,endYear):
        InvT1 = InvestmentT1_EPSPAYOUT(asset, EPSratio, p)
        invCFListY1.append(InvT1)
        EPSratio =  EPS_t2 (asset, EPSratio, InvT1, invReturnRate)
    print("\n\nSeries of re-investments from earnings, cst growth : $", str(invCFListY1))
    
    asset.data['ReInvestCFListY1']=invCFListY1
    print(asset.data['ReInvestCFListY1'])
    return invCFListY1   
#NPVt LIST GENERATOR
def NPVt_ListGen (asset, ReInvestCFListY1, invReturnRate, 
                  discRate, endYear):
    ''' 
    calculates series of NPVs for each investment in series of years.
    assumes investment return and discount rates constant
    '''
    if asset != None:
        if 'ReInvestCFListY1' not in asset.data.keys() and ReInvestCFListY1 == None:
            ReInvestListGen (asset, None, discRate, None, invReturnRate, None, endYear, None)
        elif 'ReInvestCFListY1' not in asset.data.keys() and ReInvestCFListY1 != None:
            asset.data['ReInvestCFListY1'] = ReInvestCFListY1
  
        
        
        #DEFINE FROM ASSET OR EXCEPTION
        if 'invReturnRate' not in asset.data.keys() and invReturnRate == None:
            print("invReturnRate not given for given security. ReInvestCFList not calculated.")
            return None
        elif 'invReturnRate' in asset.data.keys() and invReturnRate == None:
            #INT OR FLOAT = CONSTANT GROWTH:
            if type(asset.data['invReturnRate']) in (int, float):
                invReturnRate = asset.data['invReturnRate']
            #FILL FOR NONCONSTANT GROWTH
            else:
                print("security data for invReturnRate incorrect type. NPVtList not calculated. \n\n")
                return None
            
        if endYear in (0, None):
            print("endYear Invalid")
            return None
        if discRate is None or discRate < 0:
            print("Discount Rate Invalid")
    NPVtList = []
    print("INV RETURN RATE:", invReturnRate)
    print("REINVESTMENT LIST", str(asset.data['ReInvestCFListY1']))
    #FILL FOR VARYING INVESTMENT RETURN RATES
    for i in asset.data['ReInvestCFListY1']:
        print(i)
        npvt = -i +((invReturnRate*i)/discRate)
        NPVtList.append(npvt)
    print("LIST OF NPVs for all investments in series: $ ", str(NPVtList))
    return NPVtList
#PRICE AT TIME 0 GIVEN EPS TIME+1 etc
         
        
    
def PV0_EarningsT (asset, discRate, time, FCFListY1=None, 
                   earnings=None, PEratio=None,
                   bookValueY0=None, PBratio=None):
    
    print('FSs.PV0_EarningsT called\n')
    FCFListY1 = f_FCFListY1(asset, FCFListY1, None)
    earnings = f_Earnings(asset, earnings, None)
    bookValue = f_bookValueY0(asset, bookValueY0, None)
    
    
    PV_FCFList = FS.PVCFListGen(asset, FCFListY1, 1, discRate, time+1)
    print(earnings)
    
    if PBratio != None and bookValue != None:
        print("Calculating PV at T0 using PB Ratio and bookValueY0: \n")
        PVCF_T = ( PBratio * bookValue[time] )/((1+discRate)**time)
        sPVFCF = sum(PV_FCFList[:time])
        print(PVCF_T)
    elif PEratio != None and earnings != None:
        print("Calculating PV at T0 using PE Ratio and earnings. \n")
        try:
            PVCF_T = ( PEratio * earnings[time] ) / ((1+discRate)**time)
            print("\n\nPV of final cash flow: $", str(PVCF_T))
            sPVFCF = sum(PV_FCFList[:time])
        except: 
            print("Index error or earnings list not sufficient data for year @ time")
            return None
    elif PEratio == None and PBratio ==None: 
        print("Calculating PV at T0 using DCF and PV Time+1: \n")
        if len(earnings) > time:
            PVCF_T1 = earnings[time+1] / discRate
            print(PVCF_T1)
            PVCF_T = PVCF_T1 / ((1 + discRate)**(time+1))
            sPVFCF = sum(PV_FCFList[:time+2])
            print(sPVFCF)
            print("\nPresent Value of Final cash flow est: $", str(PVCF_T))
        else:
            print('\nEarnings data not in range for time specified.')

    else:
        print("Not sufficient data to infer PV at T0")
        return None
    PV_T0 = PVCF_T + sPVFCF
    print("\nPresent Value of asset: $", str(PV_T0))
    return PV_T0



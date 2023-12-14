# -*- coding: utf-8 -*-
"""
MITx 15.415 Fiancial Calculator
Designed to analyze security or asset data, as well as handle manual numerical input for solving financial problems.
@author: DemiAbromaitis
"""

import numpy as np
import FS_bonds as FSb
import FS_stock as FSs
from scipy.optimize import fsolve



#-----------------------------------------------------    
#!!! ASSET AND PORTFOLIO GENERATOR FUNCTIONS !!!       
#-----------------------------------------------------

#CASH FLOW FORECASTING FROM DATA ABOUT SECURITY:
def CFListFind(asset):
    if "CFListY1" not in asset.data.keys():
        if isinstance (asset, FSb.Bond):
            FSb.Bond.CFListGen(asset)
        if isinstance (asset, FSs.Stock):
            FSs.CFListGen(asset)
        else:
            print("data class type not detected")
    print('Cash flow list found or generated')
def CFListGen(CF_T, Time, CF_t1, CF_rate, CF_growthRate, CF_growthPeriods, k=1):
    
    """
    
    Parameters.
    ----------
    asset : security class data for saving entry, 
        can be None
        
    CF_T : final cash flow at time
        for bonds, face value. 
        for stocks/firms, final CF.
    Time : INT/FLOAT, year
        bonsds: time to maturity.
        stocks: end year for DCF model
    CF_t1 : FLOAT or NONE
        cash flow at given year
    CF_rate : FLOAT or NONE. annual terms
        bond: rate of coupon to face value.
        stock: 
    CF_growthRate : FLOAT, LIST OF, OR NONE. annual
        bond: rate of coupon to face value.
        stock:
    CF_growthPeriods: FLOAT, LIST OF, OR NONE years
        bond: rate of coupon to face value.
        stock:
    price : FLOAT or NONE
        current market price of security
    k: FLOAT or INT
        compound periods per year
    
    Returns.
    -------
    CFList : LIST OF FLOATS. dollars, 
        list of cash flows for year 1->T

    """
    # INITIALIZE:
    CFList = []

    # EXCEPTION HANDLING
    if CF_t1 == None and CF_rate == None:
        print("CF or CF rate must be indicated. May be zero. Check data")
        return None
    if CF_T == None:
        print("final CFT must be calculated or defined.")
        return None

    # 1 year term assumes no series of CFs
    if Time in (1, 1/k):
        CFList.append(CF_T)
        print("CFListGenDCF called. 1yr term CF:", str(CFList))       
        return CFList
        
    #ASSIGN Time for compound periods, no longer annual
    Time = Time * k
    
    # CALC CF_t1 if unspecified
    if CF_t1 in (0, None) and CF_rate not in (0, None):
        #divide annual rate by periods per year compound
        if k!= 1:
            CF_rate /= k #update rate for compound periods
            CF_t1 = CF_T * CF_rate
        else:
            CF_t1 = CF_T * CF_rate
      
    # ZERO CF FOR TERM
    if CF_t1 == 0 and CF_rate in (0, None):
        for t in range(0, Time-1):
            CFList.append(0)
        CFList.append(CF_T)
        print("CFListGenDCF called. zero CF for term.")
        print("CF LIST : $", str(CFList))
        return CFList
    

    
    # NO GROWTH
    if CF_growthRate == 0 or CF_growthRate == None:
        # series of cash flows
        for t in range(0, Time-1):
            CFList.append(CF_t1)
        # final cash flow
        CFList.append(CF_t1 + CF_T)
        print("CFListGen_DCF called. CF List: $", str(CFList))
        return CFList

    # CONSTANT GROWTH
    elif type(CF_growthRate) == float:
        # EXCEPTION
        if type(CF_growthPeriods) not in (int, float):
            print("Growth rate and growth period data mismatch. Make Periods = 1")
            return None
        #add compounding CF
        for t in range(0, Time-1):
            CFList.append(CF_t1)
            CF_t1 = CF_t1*(1+CF_growthRate)
        #add final cash flow
        entry = CF_T + (CFList[-1]*(1+CF_growthRate))
        CFList.append(entry)
        print("Constant Growth, CF List: $ \n", str(CFList))
        return CFList

    # MULTIPLE GROWTH PERIODS
    elif type(CF_growthRate) == list:
        
        #EXCEPTION HANDLING
        if type(CF_growthPeriods) != list:
            print("growth rate and growth periods must be same type. make growthPeriods list")
            print("growth rates and periods list index mismatch. check data")
        
        #ADD ADD CFS USING CORRESPONDING GROWTH RATES & TERMS
        else:
            #INITIALIZE
            print('stop1')
            for rate in CF_growthRate:
                rate /= k
            for period in CF_growthPeriods:
                period *= k
            CFList.append(CF_t1)
            TimeCount=0
            
            #for each growth period
            for term in CF_growthPeriods:
                print('stop2')
                termIndex=0
                #Limits to growth period duration 
                while termIndex in range(0, term):
                    print('stop3')
                    #while within final Time/Maturity Limit (except last CF)
                    if TimeCount < Time-2:
                        print('stop4')
                        entry = CFList[TimeCount] * (1+CF_growthRate[CF_growthPeriods.index(term)])
                        CFList.append(entry)
                    termIndex += 1
                    TimeCount +=1
            #add final CF with appropriate compounding rate
            entry = CF_T + (CFList[-1]*(1+CF_growthRate[-1]))
            CFList.append(entry)
            print("CFs with series of growth rates for given \
                  periods t: $ \n", str(CFList))
            return CFList
    
    #DATA CONDITIONS NOT PROVIDED FOR
    else:
        print("something went wrong")        
def CFArrayGen(portfolio, investT0=False, vertical=False):
    maxTerm = 0
    CFList= []
    for asset in portfolio.data['assetList']:
        print('first loop')
        CFListFind(asset)
        
                
        if maxTerm < len(asset.data['CFListY1']):
            maxTerm = len(asset.data['CFListY1'])
    
    for asset in portfolio.data['assetList']:
        entry = asset.data['CFListY1'][:]
        #make equal to longest array for linalg
        while len(entry) < maxTerm:
            entry.append(0)
        
        if investT0 == True:
            entry.insert(0, (-1*asset.data['priceT0']) )
        CFList.append(entry)
        
    if vertical==True:    
        CFArray = np.column_stack(CFList)
    else: 
        CFArray = np.array(CFList)
    return CFArray

#PRESENT VALUE OF FORECASTED CASH FLOWS FROM DATA ABOUT SECURITY:
def PVCFListGen(asset, CFList=None, compPeriods_k=1, discountRate=0, time=None): 
    #INITIALIZE
    PVCFList = []
    
    #compound periods adjustment
    if asset.data['k'] == 1 and compPeriods_k == 1:
        k =  asset.data['k'] #indicated by asset attr
    if asset.data['k'] == 1 and compPeriods_k != 1:
        k = compPeriods_k #indicated by formula call
        
    discountRate /= k
    Time = k*asset.data['Time']
            
    #find or create cash flow list:
    if CFList == None:
        #compound periods adjustment
        if asset.data['k'] == 1 and compPeriods_k == 1:
            k =  asset.data['k'] #indicated by asset attr
        if asset.data['k'] == 1 and compPeriods_k != 1:
            k = compPeriods_k #indicated by formula call
            
        discountRate /= k
        Time = k*asset.data['Time']
        
        CFListFind(asset)
        
    
        Time = len(asset.data['CFListY1'])
        if 'PVCFListY1' not in asset.data.keys():
            if type(discountRate) == float:
                
                for t in range(0 , Time):
                    entry = asset.data['CFListY1'][t]/(1 + discountRate)**(t + 1)
                    PVCFList.append(entry)
    
                    
            elif type(discountRate) == list:
                if len(discountRate) == len(asset.data['CFListY1']):
                    for t in range (0,Time): 
                        entry = asset.data['CFListY1'][t]/(1 + discountRate)**(t + 1)
                        PVCFList.append(entry)
    
            else: 
                print("discount Rate is not correct type for use")
                return None
            asset.data['PVCFListY1'] = PVCFList 
    else:
        #compound periods adjustment
            
        discountRate = discountRate / k
        Time = time * k
        
        if type(discountRate) in (int, float):
            
            for t in range(0 , Time):
                entry = CFList[t]/((1 + discountRate)**(t + 1))
                PVCFList.append(entry)

        
        #elif type(discountRate) == list:
        #    if len(discountRate) == len(CFList):
        #        for t in range (0,Time): 
        #           entry = CFList[t]/(1 + discountRate)**(t + 1)
        #            PVCFList.append(entry)
        
        else:   
            print("discount Rate is not correct type for use")
            return None
        
    print("\n\nPVCF List for single asset", str(PVCFList), '\n\n') 
    return PVCFList
def PVCFArrayGen(portfolio, investT0=False, vertical=False):
    maxTerm = 0
    PVCFList= []
    for asset in portfolio.data['assetList']:
        print('first loop PVCF')
        if 'PVCFListY1' not in asset.data.keys():
            if isinstance (asset, FSb.Bond):
                FSb.Bond.PVCFListGen(asset)
            
            #FILL IN FOR STOCK !!!
            #if isinstance (asset, FSb.Stock):
                #FSb.Stock.CFListGen(asset)
                            
        if maxTerm < len(asset.data['CFListY1']):
            maxTerm = len(asset.data['CFListY1'])
    for asset in portfolio.data['assetList']:
        entry = asset.data['PVCFListY1']
        #make equal to longest array for linalg
        while len(entry) < maxTerm:
            entry.append(0)
        
        if investT0 == True:
            entry.insert(0, (-1*asset.data['priceT0']) )
            
        PVCFList.append(entry)
        
    if vertical==True:    
        PVCFarray = np.column_stack(PVCFList)
    else: 
        PVCFarray = np.array(PVCFList)
    return PVCFarray 
def tPVCFListGen(asset, compPeriods_k=1, discountRate=0):
    print("tPVCFListGen Called")
    if asset.data['k'] not in (1, None):
        k = asset.data['k']
    else:
        k = compPeriods_k
    tPVCFList =[]
    if 'PVCFListY1' not in asset.data.keys():
        print("Must create PVCFList Entry for asset")
        asset.data['PVCFListY1'] = PVCFListGen(asset, compPeriods_k, discountRate)
    Time = len(asset.data['PVCFListY1'])
    for t in range (0, Time):
        tPVCFList.append( asset.data['PVCFListY1'][t] * ( (t+1) / k) )
    print("PVCF List called for asset")
    print("tPVCF List Generated:", str(tPVCFList))
    asset.data['tPVCFListY1'] =  tPVCFList
    return tPVCFList        
         

#SUM CF LIST FUNCTIONS
def sum_CFy1(asset, time=None):
    if time == None:
        return sum(asset.data['CFListY1'])
    else:
        sum(asset.data['CFListY1'][0:time])
def sum_PVCFy1(asset, time=None):
    print("sum_PVCF called")
    return sum(asset.data['PVCFListY1'])
def sum_tPVCFy1(asset, time=None):
    print("sum_tPVCF called")
    return sum(asset.data['tPVCFy1'])


#-----------------------------------------------------
#!!! PRESENT VALUE, CASH FLOW, AND PRICE EQUATiONS !!! 
#-----------------------------------------------------

#PRESENT VALUE - DISCOUNTED CF OF GIVEN YEAR
def PV_Div(asset, rate, time):
    '''
    Parameters
    ----------
    asset : security class instance or 
        FLOAT. dollars.
    rate : FLOAT. discount or interest rate
    time : INT. number of years to discount back
    
    Returns
    -------
    PV : FLOAT. dollars. discounted value of CF

    '''
    if type(asset) not in (int, float):
        CFListGen(asset)
        PV = asset.data['CFListY1'][time-1]/ ((1+rate)**time)
    else:
        print("asset given as int or float")
        PV = asset / ((1+rate)**time)
    return PV
#PRICE FROM LINEAR GROWTH OF CF
def Price_Residual(asset, discRate, priceYear=0, growthRate=0, growthPeriods=1):
    '''
    Parameters
    ----------
    asset : CLASS INSTANCE (security) OR INT/FLOAT (CF specified, dollars)
    discRate : FLOAT, spot rate used
    growthRate : FLOAT OR LIST OF. predicted growth rate or rates
        The default is 1.
    growthPeriods : INT OR LIST OF. # time periods/years per growth phase
        DESCRIPTION. The default is 1.
    priceYear : INT, optional. if calculating for a non-zero year price edit.
        DESCRIPTION. The default is 0.

    Returns
    -------
    PRICE OF STOCK. FLOAT. dollars, using gordon model for linear growth periods

    '''
    
    #CREATE LIST OF CASH FLOWS IF DNE
    CFListFind(asset)
    
    #GORDON MODEL OR ZERO GROWTH
    #given single Y0->Y1 data:
    if type(growthRate) in (int, float): 
        #linear growth for next stock dividend

        Divt1 = asset.data['CFListY1'][priceYear-1]
        if priceYear == asset.data['Time']:
            #adjust final CF to not have faceVal or price for perpetuity
            Divt1 -= asset.data['CF_T'] 
        print('dividend detected as: ', str(Divt1))
        #use perpetuity equation D1/(r-g), where g<r always
        P0 = PV_Perpetuity(Divt1, discRate, growthRate)
        print("Price at t=0 given div0 and growth $ : Gordon Method \n")
        return P0
    
    elif type(growthRate) == list:
        #finds dividend for priceYear-1 (index)
        Divt1 = asset.data['CFListY1'][priceYear-1]

        #Compute which growth rate corresponds to the desired year
        year = 0
        gr_t = growthRate[year]
        for term in growthPeriods:
            for t in range (0, term):
                if year <= priceYear:
                    year+=1
                    gr_t = growthRate[growthPeriods.index(term)]

        #IF RESIDUAL PRICE OF GIVEN YEAR NEEDED: use gordon model/perpetuity
        print("dividend detected is: $", str(Divt1))
        print("growthrate detected is: $", str(gr_t))
        
        P0 = PV_Perpetuity(Divt1, discRate, gr_t, False)
        print("\n\nThe residual price for year", str(priceYear), "is : $ ", str(P0))
        return P0
        
    else:
        print ("\n\nError in data type entered. Check dividend/disc rate value(s) or types(s)")

#-----------------------------------------------------
#!!! CONSTANT GROWTH RATE EQUATIONS !!! 
#-----------------------------------------------------

#CALCULATE THE CONSTANT GROWTH RATE GIVEN Y1 DIVIDEND AND INT RATE
def GrowthRate_CG (asset, discRate, priceT0):
    '''
    Parameters
    ----------
    asset CLASS INSTANCE (or dividend entry) FLOAT, $ dividend1
    
    discRate : interest rate presumed for period
        assumes constant discount rate
    priceT0 : FLOAT. dollars, current value or market price of stock
        if None, indicated by asset dictionary
    
    Returns
    -------
    g : FLOAT. % as decimal. growth for dividend
    '''
    if type(asset) in (int, float):
        if priceT0 == None:
            print("Price must be entered unless asset is class")
        else:
            dividendT1 = asset
    else:
        if priceT0 == None and 'priceT0' not in asset.data.keys():
            print("price must be indicated by class or function")
            return None
        elif priceT0 == None and 'priceT0' in asset.data.keys():
            priceT0 = asset.data['priceT0']
        dividendT1 = asset.data['CF_t1']
        print('priceT0 detected as: $', str(priceT0))
        print('dividendT1 detected as: ', str(dividendT1))
        print('dividend to price ratio is:')
        print(dividendT1/priceT0)
        #EXCEPTION HANDLING
        if dividendT1 == 0:
            return 0
            
    g = discRate - (dividendT1/priceT0)
    print("GrowthRate_CG Called. \nGrowth Constant, from price, div, rate: ", str(g))
    return g
#CALCULATE EXPECTED RETURN : CONSTANT GROWTH OF DIVIDEND
def ExpR_CstGrowth(asset, priceT0, growthRate=0):
    '''
    Parameters
    ----------
    dividendT0 : FLOAT. dollars, first expected dividend (assume year 1)
    priceT0 : FLOAT. dollars, current price or value as given or calculated
    growthRate : FLOAT. growth rate for given year T0-> T1

    Returns
    -------
    r : FLOAT. dollars, given expected return from T0-> T1

    '''
    print("expected return from constant growth called for asset")
    #if asset entered is the CF value:
    if type(asset) in (int, float): 
        CF_1 = asset *(1+growthRate)
        r = (CF_1 / priceT0) + growthRate
        print("Expected return r calculated from d1, p0, growthRate")
        return r

    else: 
        growthRate = asset.data['CF_growthRate']
        CFListFind(asset)
        if type(growthRate) not in (int, float):
            if type(growthRate) == None:
                growthRate=0
            else:
                print('growth rate data of asset is not int or float')
        print("class growth rate detected as: ", str(growthRate))
        

        CF_1 = asset.data['CFListY1'][0]
        print("Cash Flow detected as: ", str(CF_1))
        if priceT0 == None:
            try:
                priceT0 = asset.data['priceT0']
            except:
                print("Price Data not indicated")
        print("priceT0 indicated as : ", str(priceT0))
        r = (CF_1 / priceT0) + growthRate
        print("Expected return r calculated from d1, p0, growthRate")
        return r                
#CALCULATE EXPECTED RETURN FROM DP RATIO
def ExpR_CG_DPratio (asset, DPratio, growthRate):
    '''
    Parameters
    ----------
    DPratio : FLOAT. ratio $/$ of dividend to current price of stock
    growthRate : FLOAT. growth rate for given period,
        assumes constant growth, treats value as perpetuity

    Returns
    -------
    r : FLOAT. dollars, expected return

    '''
    if asset != None:
        if 'DPratio' in asset.data.keys():
            DPratio = asset.data['DPratio']
        else:
            print("DP ratio not indicated by class")
        if 'CF_growthRate' in asset.data.keys():
            if type(asset.data['CF_growthRate']) in (int, float):
                    growthRate = asset.data['CF_growthRate']
            else:
                print("can't use growth rate from class instance")
    r = (1+growthRate)*DPratio + growthRate
    print("expected return, r on stock, calculated from DP ratio")
    return r
#
#-----------------------------------------------------
#!!!  DURATION EQUATIONS !!! 
#-----------------------------------------------------


#DURATION DATA LIST MOD
def DurationData_list(portfolio, rate, compPeriods_k):
    '''
        input: listed bonds, k comp periods, yield or interest rate
        return: sum of list of PVs from CFs from Portfolio of assets
    '''
    PVCF = []
    tPVCF = []
    
    for asset in portfolio.data['assetList']:
        CFListFind(asset)
        asset.data['tPVCFListY1'] = tPVCFListGen(asset, compPeriods_k, rate)
        PVCF.append( asset.data['PVCFListY1'] )
        tPVCF.append( asset.data['tPVCFListY1'] )
    
    """
    elif type(rate) == list:
        #Generate DurationData
        for asset in portfolio:
            x, y = Bond.DurationData_RateList(bond, compoundPeriods, rate)
            PVCF.append(x)
            tPVCF.append(y)
    """
    
        
    #debug reporting
    print("PV(Cf) of Portfolio:")
    print(str(PVCF), "\n")
    print("Time weighted PV(Cf)s of Portfolio")
    print(str(tPVCF), "\n")
    sPVCF, stPVCF = 0, 0
    for pvals in PVCF:
        for val in pvals:
            sPVCF += val
    for tpvals in tPVCF:
        for val in tpvals:
            stPVCF += val

    print("Sum of PV(Cf) of Portfolio:")
    print(str(sPVCF), "\n")
    print("Sum of Time weighted PV(Cf)s of Portfolio")
    print(str(stPVCF), "\n")
    return [sPVCF, stPVCF]      
#MACAULAY
def MacaulayDuration (asset, discRate, compPeriods_k=1):
    ''' 
    Input: bond data, pay periods per yr, bond yield as float
    Returns: duration of bond in terms of years
    ''' 
    print("\n Macaulay Duration Called")
    CFListFind(asset)
    if "tPVCFListY1" in asset.data.keys():
        tPVCFsum = sum(asset.data["PVCFListY1"])
    else:   
        tPVCFsum = sum(tPVCFListGen(asset, compPeriods_k, discRate))
  
    
  
    if 'Price' in asset.data.keys():
        Price = asset.data['Price']
    elif isinstance (asset, FSb.Bond) == True:
        Price = sum( asset.data['PVCFListY1'])
        
        
    #returns DURATION, as num of periods
    if Price in (0, None):
        print("No price for asset: ")
        return None
    if compPeriods_k <= 0:
        print("k out of range (k>0)")
        return None
    D = tPVCFsum/Price
    #modify for non-annual compounding
    D_years = D/compPeriods_k 
        
    #debug reporting
    print("Macaulay Duration in year terms;")
    print(str(D_years), "\n")
    return D_years
#MODIFIED DURATION FROM CF & MACAULAY   
def ModifiedDuration (asset, discRate, compPeriods_k=1,):
    ''' 
    input: bond data, compoundPeriods, bond yield as float
    if annual, compoundPeriods=1
    returns: duration of a bond in terms of years
    '''
    D = MacaulayDuration(asset, compPeriods_k, discRate)
    #returns DURATION
    #in terms of periods for solution:
    MD = (D*compPeriods_k)/(1+(discRate/compPeriods_k))
    #convert to per annum for resuCALlt
    MD_years = MD/compPeriods_k
    
    #debug reporting
    print("Modified Duration in year terms:")
    print(str(MD_years), "\n")
    return MD_years
#CALCULATE MACAULAY DURATION FOR LIST OF ASSETS
def MacaulayDuration_list (portfolio, intYieldRate, compPeriods_k=1):
    '''
    input: listed bond data, k compounding periods, yield or interest rate
    output: duration in terms of years
    '''
    sPVCF, stPVCF =  DurationData_list( portfolio,
                                        intYieldRate,
                                        compPeriods_k)
    D = stPVCF / sPVCF
    #modify for non-annual compounding
    D_years = D / compPeriods_k 
    #debug reporting
    print("Macaulay Duration in year terms;")
    print(str(D_years), "\n")
    return D_years
#CALCULATE MODIFIED DURATION LIST FROM CF & MACAULAY   
def ModifiedDuration_list (portfolio, intYieldRate, compPeriods_k=1):
    ''' 
    input: bond data, compoundPeriods, bond yield as float
    if annual, compoundPeriods=1
    returns: duration of a bond in terms of years
    '''
    k = compPeriods_k
    D = MacaulayDuration_list(portfolio, intYieldRate, compPeriods_k)
    #returns DURATION
    #in terms of periods for solution:
    MD = (D*k)/(1+(intYieldRate/k))
    #convert to per annum for resuCALlt
    MD_years = MD/k
    
    #debug reporting
    print("Modified Duration in year terms:")
    print(str(MD_years), "\n")
    return MD_years  


#-----------------------------------------------------      
#!!! ELASTICITY AND INTEREST RATE LISTS !!!
#-----------------------------------------------------

#CALCULATE COUPON BOND PRICE FROM SPOT INTEREST RATE LIST
def Price_IntRateList(asset, intRateList, rateChange=0):
    ''' 
    uses spot rate trend list, coupon and principal, maturity
    to solves for current price of Coupon Bond
    if rateChange = FLOAT is indicated, it will alter intRateList.
    '''
    #EXCEPTION HANDLING
    print("Bond price from IntRateList called")
    if type(intRateList) != list:
        print("intRateList value must be of list type")
        return None
    #INITIALIZE
    k= asset.data['k']
    B=0 #initalize bond price
    CFListFind(asset)
    
    
    if rateChange != 0:
            print("Must alter rate list to account for change")
            rateList = RateListChangeGen(intRateList, rateChange)
    else:
        rateList = intRateList
    T= len(asset.data['CFListY1'])
    for t in range (0, T):
        B += asset.data['CFListY1'][t] / ((1+rateList[t])**((t+1)/k))
        print(B)
    print("Current Coupon Bond Price: $ ", str(B))
    return B
#PRICE ELASTICITY = MODIFIED DURATION, SOLVES SAME WHEN INT IS FLAT 
def PriceElast_MD(asset, oldPrice, rate, rateChange, compPeriods_k=1):
    ''' 
        input: original bond data, rate change (annual), and new price after rate change
        returns: MD = abs val of Price elasticity
        assumes that yield curve is flat or changes in parallel
        set rate change to zero if not checking price elasticity before and after
        
    '''
    #debug reporting
    print("Price elasticity from modified Duraiton Called")
    
    #DEFINE DATA
    k = compPeriods_k

    
    #if only function inputs specify price
    if asset.data['priceT0'] in (0, None) and \
        oldPrice not in (0, None):
            print("price (before change) indicated")
            B = oldPrice
    #if price not indicated and must be calculated
    elif asset.data['priceT0'] in (0, None) and oldPrice in (0, None):
            print('price calculated from int rate list')
            B = Price_IntRateList(asset, rate)

    else:
        print("price indicated by asset")
        B = asset.data['priceT0']

    #compute if not found:
    CFListFind(asset)
    #calculate present value based on yield, t+1 in denominator
    pvcfList = [] #initialize list
    T= len(asset.data['CFListY1'])
    
    
    #Time is +2 in this formula. ! don't use PVCFListGen !
    for t in range(0, T):
        if type(rate) == float:
            pvcfList.append(asset.data['CFListY1'][t]/(1+rate)**((t+2)/k))
        elif type(rate) == list:
            pvcfList.append(asset.data['CFListY1'][t]/(1+rate[t])**((t+2)/k))
    #store as special PVCFListY1_rc
    asset.data['PVCFListY1_rc'] = pvcfList #assigns to data
    #sum should be equal to bond final cash flow
    PVsum = sum(pvcfList)
        
    #debug reporting
    print("Bond Cash Flow PVs: ")
    print (str(pvcfList), "\n")
    print("Sum of Cash Flow PVs: ")
    print(str(PVsum), "\n")
        

    #Calculate t * PV(CFt) ! Special Input, do not use tPVCFListGen() !
    #Weighted Value of Payment tenors
    tPVCFList = []
    for t in range (0, T):
        tPVCFList.append(asset.data['PVCFListY1_rc'][t] * (t+1))
    tPVCFsum = sum(tPVCFList)
   
    #debug reporting
    print("Weighted PV(CFt)s")
    print(str(tPVCFList), "\n")
    print("Sum of t*PV(CFt):")
    print(str(tPVCFsum), "\n")
   
    PE = (1/B)*tPVCFsum
    print("\n If yield curve flat, MD = |PE|. PE = ", str(PE), "\n\n")
    asset.data['PEratio'] = PE
    return PE
#PICE CHANGE due to elasticity
#   COMPUTE EST PRICE CHANGE - INTEREST SHIFT & PRICE ELASTICITY (before rate change)
def PriceChange_Elast_Linear(asset, oldPrice, rate, rateChange,
                             compPeriods_k=1):
    ''' 
        parameters: 
            bond data, 
            if B (price, float) is calculated separately, 
            unchanged rate(s) (float or list of floats), 
            rate change, float range (-1, 1),
            k periods (int or float) default 1 per year,
        returns: 
            change in price B when rates change
        assumes: 
            rate change is parallel to curve, or rate is flat
    '''  
    print("Price Change Due to Elasticity (Linear Model) Called")
    #DEFINE VARIABLES
    if 'PEratio' not in asset.data.keys():
        PriceElast_MD (asset, oldPrice, 
                       rate, rateChange, 
                       compPeriods_k=1)
    else:
        PE = asset.data['PEratio']
    print("price elasticity: ", str(PE))


    print('Price must be calculated from int rate list')
    B0 = Price_IntRateList(asset, rate)

    dB= -1* B0 * abs(PE) * rateChange
    print("/n The change in price from price elasticity is: $", str(dB))
    return dB
#CALCULATE % CHANGE IN PV OR PRICE
def ValueChange_ModDuration(asset, intYieldRate, rateChange, compPeriods_k):
    ''' 
    input: data for (bond, security) asset class instance.
        yield or interest, 
        rate change,
        k comp periods : default=1
    output: percent change in PV or Price
    '''
    MD=ModifiedDuration(asset, intYieldRate, compPeriods_k)
    valueChange = (-MD/100)*(rateChange)
    print("Change in PV or Price of bond: ")
    print("%", str( valueChange*100 ), "\n")
    return valueChange
#CHANGE IN PV OR PRICE USING MOD DURATION    
def PVChange_ModDuration_list(portfolio, intYieldRate, rateChange, compPeriods_k=1):
    sPV, stPV = DurationData_list(portfolio, intYieldRate, compPeriods_k)
    print("\n","sPV(CF) = ", str(sPV), "\n")
    MD = ModifiedDuration_list(portfolio, intYieldRate, compPeriods_k)
    print("MD = ", str(MD), "\n")
    dr = rateChange
    print("dr =", str(dr), "\n")
    dPV = sPV * -MD *(dr)
    print("Change in PV via ModDuration: $:", str(dPV), "\n")
    return dPV
#CALCULATE % CHANGE IN PV OR PRICE
def ValueChange_ModDuration_list(portfolio, intYieldRate, rateChange, compPeriods_k=1):
    ''' 
    input: listed asset data, k comp periods, yield or interest, rate change
    output: percent change in PV or Price
    '''
    MD=ModifiedDuration_list(portfolio, intYieldRate)
    valueChangeRatio= (-MD)*(rateChange)
    print("% Change in PV or Price of portfolio (as ratio): \n")
    print(str(valueChangeRatio))
    return valueChangeRatio




#-----------------------------------------------------
#!!! NOMINAL INTEREST RATE FUNCTIONS
#-----------------------------------------------------

#NOMINAL RATES SOLVERS
def nom_rate(realRate, inflationRate):
    return ((1+realRate)*(1+inflationRate))-1
# FUTURE VALUE FROM NOMINAL RATE
def nom_futureValue(presentVal, realRate, inflationRate, time):
    # inputs are floats
    return (presentVal * (((1+realRate)*(1+inflationRate))**time))
# NOMINAL PRESENT VALUE - future value and return known
    # for real terms, use real rate and make inflationRate=0
def nom_presentValue(futureVal, realRate, inflationRate, time):
    # inputs are floats
    return futureVal / (((1+realRate)*(1+inflationRate))**time)
    # returns float - dollars


#-----------------------------------------------------    
#!!! RATE & RATE CHANGE SOLVERS !!!
#-----------------------------------------------------

#INTEREST RATES LINEAR CHANGE
def RateListChangeGen(rateList, rateChange):
    rateListNew =[]
    if type(rateList) == float:
        rateNew = rateList*rateChange
        return rateNew
    elif type(rateChange) == float:
        for rate in rateList:
            rateListNew.append(rate+rateChange)
    else:
        print("data provided is not correctly formatted \n \
              Check that RateList is FLOAT OR LIST and rateChange is FLOAT")
    return rateListNew
#ANNUAL PERCENTAGE RATE TO EFFECTIVE ANNUAL RATE
def APRtoEAR(APR, k):
    '''
    Parameters
    ----------
    APR : Annual rate of interest
    k : Float or Int. compounding periods per year
        must be >0
    Returns
    -------
    EAR : Float. effective or equivalent annual rate. 
    '''
    return (1 + APR/k)**k - 1
#YIELD TO MATURITY FROM FORECASTED INTEREST RATE LIST
def YieldToMaturity(asset, InterestRateList):
    ''' 
    Estimates Yield to Maturity using a list of spot interest rates
        for bonds with varying maturity
    
    Input: bond data, list of interest rates for Y1>>T
    Returns: YTM % as float. 
    '''
    
    #generate bond price from interest rate list
    B = Price_IntRateList(asset, InterestRateList)
    
    #INHERENT
    high = max(InterestRateList)
    low = min(InterestRateList)
    guess = (high+low)/2
    iterations=0
    epsilon=.00001
    
    #YTM BISECTION SUBFUNCTION - use bisection search to estimate values of YTM that make B == B(ytm)
    def YTM_bisection(asset, guess, iterations, 
                      high, low, epsilon):
        YTM=[]
        for t in range(0, asset.data['Time']):
            YTM.append(guess)
            
        #debug reporting:
        print("iteration: ", str(iterations))
        print("guess: ", str(guess))
        
        #initial function call
        Bguess = Price_IntRateList(asset, YTM)
        
        #Bisection Loop moderated 
        #via num of iterations and epsilon variance tolerance
        #comparison reflects inverse relationship between B and YTM
        while iterations<30:
            if Bguess - B <= -epsilon:
                high =guess
                
            elif Bguess - B >= epsilon:
                low = guess
            else:
                print("Solution: \n")
                print("The YTM on the bond is:")
                print(guess)
                return guess
            iterations+=1
            guess=(high+low)/2
            
            #recursive call
            return YTM_bisection(asset ,guess,iterations, 
                                 high, low, epsilon)
    YTM_bisection(asset, guess, iterations, 
                  high, low, epsilon)
#CALCULATE SPOT RATES FROM LIST OF BOND DATA
#SOLVES FOR LIST OF RATES rs               
def SpotRateArray(portfolio):
    ''' 
    takes in a list of bond data
        prices or PV known, Cash Flows Known
    returns array of interest rate %s as floats
    
    '''
    #GENERATE ARRAYS FOR KNOWN VALUES - Price, T, and CF
    CF = CFArrayGen(portfolio)
    print("CF array")
    print(str(CF), "\n")
    Price  = GenArray(portfolio, 'priceT0')
    print("Price array")
    print(str(Price), "\n")
    time=[]
    maxTerm=0 
    for asset in portfolio.data['assetList']:
        if maxTerm < asset.data['Time']:
            maxTerm = asset.data['Time']
    for i in range (0, maxTerm):
        time.append(i+1)
    T = np.array(time)
    print("T array")
    print(str(T), "\n")
    #DEFINE NONLINEAR EQUATION ITERATIONS
    def Rs_matrix(rs):
        #create empty matrix of correct size            
        F=np.empty((maxTerm))
        #Iterated F(x)=0 for nonlinear equations  
        #added to array as entries.
       
        """
        for c in range (0, maxTerm): #cf index
            F[c] = 0
            for t in range(0, maxTerm): #time index
                F[c] += CF[c][t] /((1+rs[t])**T[t])
                print(F[c])
            F[c] += Price[c]
        """
      
        F[0]= CF[0][0]/((1+rs[0])**T[0]) \
            + CF[0][1]/((1+rs[1])**T[1]) \
                -Price[0] \
                    + CF[0][2]/((1+rs[2])**T[2]) \
                
        F[1]= CF[1][0]/((1+rs[0])**T[0]) \
            + CF[1][1]/((1+rs[1])**T[1]) \
                - Price[1] \
            + CF[1][2]/((1+rs[2])**T[2]) 

        F[2]= CF[2][0] / ((1+rs[0])**T[0]) \
            + CF[2][1] / ((1+rs[1])**T[1]) \
            + CF[2][2] / ((1+rs[2])**T[2]) \
            - Price[2]
       
        #return array of equations
        return F
    #NONLINEAR SOLVER USING SYMPY FSOLVE
    #MODIFY IF RANGE IS LONG
    rsGuess = np.array([.05, .05, .05])
    spotRateArray = fsolve(Rs_matrix, rsGuess)
    print('Spot rates for Year 0-MaxTime given portfolio of securities: \n', str(spotRateArray))
    return spotRateArray    


#-----------------------------------------------------
#!!! LINEAR ALGEBRA SOLVERS
#-----------------------------------------------------

#CREATE ARRAY, 1 DIMENSION, FOR LINALG SOLVERS    
def GenArray(portfolio, keyString, index=0):
    '''
    Parameters
    ----------
    portfolio : list of dictionaries of assets
    keyString : 'string' of specified attribute
    index : int, optional. default 0

    Returns
    -------
    ValuesArray : NP.ARRAY (1 dimensional list of list)
        lists values selected in same order as portfolio
    '''
    assetList = portfolio.data['assetList']
    ValueList = []
    for asset in assetList:
        if keyString not in asset.data.keys():
            print("Given attribute is not in given asset: \n", str(asset), str(keyString) )
        if type(asset.data[keyString]) in (float, int):
            ValueList.append( asset.data[keyString] )
        elif type(asset.data[keyString]) == list:
            print("list of float or int values detected")
            ValueList.append( asset.data[keyString][index] )
        else: 
            print("selected data for array is not of correct type: int, float, or a list of.")
    ValuesArray = np.array(ValueList)
    print("ArrayGen_1D Called. One dimensonal array = \n", str(ValuesArray))
    return ValuesArray
#SOLVE RELATIVE PRICE OF A SECURITY FROM SIMILAR CF, PRICE DATA
def RelPrice_LinAlg(portfolio, year):
    #CHANGE: if not 
    priceArray = GenArray(portfolio.data['assetList'], 'priceT0', year)
    CFsArray = CFArrayGen(portfolio.data['assetList'])
    x = np.linalg.solve(CFsArray, priceArray)
    return x
#SOLVE POSITIONS FOR SECURITIES GIVEN DESIRED CF LIST OR TIMELINE    
def PortfolioPositionsY0_CFs (portfolio, returnCFList):

    CFsArray = CFArrayGen(portfolio, True, True)
    print('Portfolio Cash Flow Array, starts with Y0 investment: $\n', str(CFsArray))
    ReturnsArray = np.array(returnCFList)
    x=np.linalg.solve(CFsArray, ReturnsArray)
    print("Portfolio Positions for Y0 investments for desired cash flow timeline: \n", str(x))
    return x


#-----------------------------------------------------
#!!! ARROW DEBREU SECURITY MODEL SOLVERS
#-----------------------------------------------------

#ARROW-DEBREU SOLVERS:
def AD_ExpReturn(asset):
    '''
    CALCULATE EXPECTED RETURN OF ASSET GIVEN FUTURE STATES
   -- Parameters:
    asset : dictionary of AD asset states
   -- Returns
    ExpR : Expected return of AD asset, float /dollars
    '''
    print("AD_ExpReturn Called")
    ExpR = 0
    numStates = len(asset.data['ArrowDebreu'])
    print('Number of arrow-debreu states', str(numStates-1))
    if asset.data['ArrowDebreu'] == None:
        print("No Data to analyze")
        return None
    for state in range(1, numStates):
            ExpR += (asset.data['ArrowDebreu'][state][0]) * (asset.data['ArrowDebreu'][state][1])
    print(ExpR)
    return ExpR
def AD_ExpReturnRate(asset):
    '''
    CALCULATE EXP RETURN RATE FOR GIVEN ASSET FUTURE STATES
   -- Parameters:
    asset : dictionary of AD asset states
   -- Returns
    r : Expected rate of return of AD asset, float (% as decimal)
    '''
    print("AD_ExpReturnRateCalled")
    if asset.data['ArrowDebreu']!=None:
        ExpR = AD_ExpReturn(asset)
        P = asset.data['ArrowDebreu'][0][0]
        r = (ExpR / P) - 1
        print('Expected return for ArrowDebreu Security: $', str(r))
        return r
    else:
        print("No Arrow Debreu Data for Asset")
        pass
def AD_VarReturn(asset):
    '''
    VARIANCE OF RETURN GIVEN MEAN EXPECTED RETURN
    -- Parameters:
    asset : dictionary of AD asset states
    -- Returns
    VarR : Variance from expected rate of return of AD asset, 
            float (% as decimal)
    '''
    print('AD_varReturn called')
    varR = 0
    if 'ArrowDebreu' not in asset.data.keys():
        print("no data")
        return None
    numStates = len(asset.data['ArrowDebreu'])
    for state in range(1, numStates):
        varR += asset.data['ArrowDebreu'][state][1] * \
            ((asset.data['ArrowDebreu'][state][0] - AD_ExpReturn(asset))**2)
    print('Variance of returns of ArrowDebreu Security: ', str(varR), "\n\n")
    return varR
def AD_sDevReturn(asset):
    '''
    STANDARD DEVIATION FROM MEAN EXPECTED RETURN
    -- Parameters:
    asset : dictionary of AD asset states
    -- Returns
    sdev : Standard Deviation from expected rate of return of AD asset, 
            float (% as decimal)
    '''
    if 'ArrowDebreu' not in asset.data.keys():
        print("No Arrow Debreu Data for asset")
    else: 
        sdev = AD_VarReturn(asset)**(.5)
    print('stDev of ExpReturns for ArrowDebreu Security: ', str(sdev))
    return sdev


#-----------------------------------------------------
#!!!PERPETUITY & ANNUITY SOLVERS
#-----------------------------------------------------

def PV_Perpetuity(asset, interestRate, growthRate=0, startY0=False):
    '''
    parameters: 
        asset, class data for security or cash flow if integer
        startY0, default false. boolean
    return: 
        present value of perpetual payments given growth rate, 
        annual interest, dollars
    consider that growth may be 0%,
    consider if payments start now (Y0) or next year (Y1)
    '''
    #allows for number entry instead of class data
    if type(asset) in (int, float):
        perpetuity = asset
        g = growthRate
    
    #PULL INFO FROM CLASS DATA
    else:
        # FIND CASH FLOW
        if asset.data['CF_t1'] in (0, None):
            if asset.data['CF_rate'] not in (0, None):
                perpetuity = asset.data['CF_rate']*asset.data['CF_T']
                print('')
            else:
                print("either CF_rate or CF_t1 must be entered for asset to solve problem")
                return None
        elif type(asset.data['CF_t1']) == float:
            perpetuity = asset.data['CF_t1']
            
        # FIND  GROWTH RATE    
        if asset.data['CF_growthRate'] in (0, None):
            g=0
        elif type(asset.data['CF_growthRate'])  == float:
            g=asset.data['CF_growthRate']
        else:
            print("wrong growth rate data type for calculation")
            return None
        
    
    if startY0 == False:
        return perpetuity/(interestRate-growthRate)
    if startY0 == True:
        # payments start Y0
        return payment + (perpetuity/(interestRate - growthRate))     
def PV_Annuity(payment, discountRate, riskFreeRate, time):
    return (payment/(discountRate-riskFreeRate)) * (1 - (((1+riskFreeRate)**time)/(1+discountRate)**time))
def PV_Annuity_Growth(payment, growth, inflation, time):
    '''
    present value of growting annuity
    growth/return of fund, plus inflationary adjustment
    assumes payments start Y1
    '''
    return payment * ((1+inflation)/(growth-inflation)) * (1 - (((1+inflation)**time)/((1+growth)**time)))
def PV_k_Annuity(payment, EAR, k_periods, num_payments):
    '''
    present value of monthly payments given EAR, period interval, and num payments
    IF PAYMENTS MONTHLY, k_periods = 12, etc.
    '''
    rate_periodic = ((1+EAR)**(1/k_periods)) - 1
    return (payment/(rate_periodic)) * (1 - 1/((1+rate_periodic)**num_payments))
def Payment_Annuity(presentValue, discountRate, riskFreeRate, time):
    return (presentValue*(discountRate - riskFreeRate)) / (1 - ((1+riskFreeRate)**time / (1+discountRate)**time))



#-----------------------------------------------------
#!!! USER INPUT SOLVERS
#-----------------------------------------------------
#FUTURE VALUE, MEAN RETURN GIVEN FV, AND FV WITHOUT COMPOUNDING
def futureValue():
    # assumes compounding interest
    # USE 1 to get a ratio # to present value (multiple)
    pVal = float(input('Enter present value in dollars:  '))
    rate = float(input('Enter rate of return as decimal:  '))
    time = int(input('Enter maturity term in years:  '))
    return round((pVal * ((1+rate)**time)), 5)
# WITHOUT COMPOUND INTEREST, ONLY ON PRINCIPAL
def futureValue_noncomp():
    # USE 1 to get a ratio # to present value (multiple)
    pVal = float(input('Enter present value in dollars:  '))
    rate = float(input('Enter rate of return as decimal:  '))
    time = int(input('Enter maturity term in years:  '))
    return round((pVal * rate * time), 3)
# AVERAGE RATE OF RETURN IN PERIOD:
def meanReturn():
    pVal = float(input('Enter present value in dollars:  '))
    fVal = float(input('Enter future return in dollars:  '))
    time = int(input('Enter maturity term in years:  '))
    return round(float(((fVal/pVal)**(1/time))-1), 4)









            
            
        
        
        
        
        
        
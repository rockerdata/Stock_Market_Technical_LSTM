import numpy as np
import tulipy as ti
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import requests
import json

#Average Directional Index

def get_ADX(high, low, close, signal):
    adx = np.zeros(len(high))
    di = np.zeros([2,len(high)])
    adx[signal*2-2:] = ti.adx(high, low, close, signal)
    di[:,signal-1:] = np.array(ti.di(high, low, close, signal))
    return [adx, di[0], di[1]]

#Aroon Oscilations

def get_ArronOSC(high, low, signal):
    aroon = np.zeros(len(high))
    aroon[signal:] = ti.aroonosc(high, low, signal)
    return aroon

#MACD
# Returns numpy array with shape (3, data_length)
def get_MACD(close, slow_signal, fast_signal, signal):
    macd = np.zeros([3,len(close)])
    macd[:,fast_signal-1:] = ti.macd(close, slow_signal ,fast_signal, signal)
    return macd

#RSI

def get_RSI(close, signal):
    rsi = np.zeros(len(close))
    rsi[signal:] = ti.rsi(close, 9)
    return rsi

#Stochastic Oscillator
# Return numpy array with shape (2, data_length)
def get_StochOsc(high, low, close, k_period, k_slow_period, d_period):
    stoch = np.zeros([2,len(close)])
    stoch[:,k_period + max(k_slow_period,d_period) + 1:] = np.array(ti.stoch(high, low, close, k_period, k_slow_period, d_period))
    return stoch
    
#Bollinger Bands
# return numpy array with shape (3, data_length)
def get_BollingerBands(close, signal, stddev):
    bbands = np.zeros([3, len(close)])
    bbands[:,(signal-1):] = np.array(ti.bbands(close, signal,stddev))
    return bbands

#On Balance Volume
def get_OBV(close, volume):
    obv = np.zeros(len(close))
    obv = ti.obv(close, volume)
    
    
#Accumulation / Distribution Line
def get_ADL(high, low, close, volume):
    adl = np.zeros(len(high))
    adl = ti.ad(high, low, close, volume)
    
#Chaikin Money Flow
def get_ChaikinMF(close, low, high,volume, period):
    money_flow_mul = ((close - low) - (high - close)) / (high -low)
    money_flow_vol = pd.Series(money_flow_mul * volume)
    cmf = money_flow_vol.rolling(period).sum() / pd.Series(volume).rolling(period).sum()
    return cmf

#Klinger Volume Indicator
def get_KVI(high, low, close, volume, slow_signal, fast_signal):
    kvo = np.zeros(len(high))
    kvo[1:] = ti.kvo(high, low, close,volume, slow_signal, fast_signal)
    kvo_signal = pd.Series(kvo).rolling(9).mean().values
    return [kvo, kvo_signal]
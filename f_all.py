from members_functions.f_bevs import *
from members_functions.f_eunice import *
from members_functions.f_shawn import *
from members_functions.f_renzo import *
from members_functions.f_dan import *

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import geopandas as gpd
import folium
from streamlit_folium import folium_static 
import warnings
warnings.filterwarnings('ignore')

def testConnection():
    print("Running f_all...")
    testDan()
    testRenzo()
    testBevs()
    # testEunice()
    testShawn()

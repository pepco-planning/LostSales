import pandas as pd
import os
import tqdm
import time

folderPath = r'C:\All\Python Projects\testy'




tab = ['a','b','c','d','a','b','c','d','a','b','c','d','a','b','c','d','a','b','c','d']


tloop = tqdm.tqdm(tab)
for t in tloop:
    tloop.set_description("Processing %s" % t)
    time.sleep(1.5)


from cgi import print_directory
from multiprocessing.dummy import Value
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import pandas as pd
import hashlib
import base64
import xlsxwriter
import os

# coding:utf-8
# sabri-kozluWebScraping
driver = webdriver.Chrome()
sektorlerList = []
url = "https://www.kgk.gov.tr/SektorVerileri"
driver.get(url)
time.sleep(5)  


sektorDegistir = Select(driver.find_element(By.ID, value="cmbSector"))
sektorSecimi =  driver.find_element(By.ID, value="cmbSector")
sektorSecimiOptions = sektorSecimi.find_elements(By.TAG_NAME, "option")
df = pd.DataFrame(columns=['Id', 'SektorAdi', 'ParentId'])
id=0;
kirilim=0;
birinciKirilim=0;
ikinciKirilim=0;
ucuncuKirilim=0;
parentid=0;


for sektor in sektorSecimiOptions:
    if(sektor.text=="Tümü"): continue; print("Tümünü Geçti");
   
    id+=1;
    sektorDegistir.select_by_value(sektor.get_attribute("value"));
    if("- -" not in sektor.text and "- - -"not in sektor.text):
        print("1. Kırılım"+sektor.text+str(parentid))
        birinciKirilim=0;
        ikinciKirilim=id;
        kirilim+=1;
        parentid=birinciKirilim;
    elif("- -"  in sektor.text and "- - -"not in sektor.text):
        print("2. Kırılım"+sektor.text+str(parentid))
        parentid= ikinciKirilim
        ucuncuKirilim=id;
    elif("- - -" in sektor.text):
        print("3. Kırılım"+sektor.text+str(parentid))
        parentid=ucuncuKirilim;
    df.loc[id] = id,sektor.text,parentid;
   
print(df);
xlWriter = pd.ExcelWriter("SektorList" + '.xlsx', engine='xlsxwriter');
df.to_excel(xlWriter, sheet_name='Sheet{}'.format(1));
xlWriter.save(); 
     


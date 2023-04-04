
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
time.sleep(15)  

yildegistir = Select(driver.find_element(By.ID, value="cmbYear"))
yilSecimi =  driver.find_element(By.ID, value="cmbYear")
yilSecimiOptions = yilSecimi.find_elements(By.TAG_NAME, "option")

raporlamaTuruDegistir = Select(driver.find_element(By.ID, value="cmbFinancialReportFrameworkType"))
raporlamaTuruSecimi =  driver.find_element(By.ID, value="cmbFinancialReportFrameworkType")
raporlamaTuruSecimiOptions = raporlamaTuruSecimi.find_elements(By.TAG_NAME, "option")

sektorDegistir = Select(driver.find_element(By.ID, value="cmbSector"))
sektorSecimi =  driver.find_element(By.ID, value="cmbSector")
sektorSecimiOptions = sektorSecimi.find_elements(By.TAG_NAME, "option")


for yil in yilSecimiOptions:
    print(yil.text);
    yildegistir.select_by_value(str(yil.text));
    time.sleep(5)
    dir = os.path.join("C:\\","Users\sabri\KGKWebScraping\Bilanco\\");
    if not os.path.exists(dir):
      os.mkdir(dir)
    for raporlamaTuru in raporlamaTuruSecimiOptions:
       if(raporlamaTuru.text=="Tümü"): continue; print("Tümünü Geçti");
       elif(raporlamaTuru.text=="TFRS"): raporlamaTuruDegistir.select_by_value(str(1)); print("Tfrs");
       elif(raporlamaTuru.text=="BOBİ FRS"):raporlamaTuruDegistir.select_by_value(str(2)); print("Bobi");
       time.sleep(5)
       for sektor in sektorSecimiOptions:
        if(sektor.text=="Tümü"): continue; print("Tümünü Geçti");
        print(sektor.text);
        sektorDegistir.select_by_value(sektor.get_attribute("value"));
        time.sleep(10)
        try:
          bilancoTable = driver.find_element(By.ID, "generaated_table").get_attribute("outerHTML")
          bilancoDf = pd.read_html(bilancoTable)
          bilancoTableExcel = pd.DataFrame()
          col_baslik = bilancoDf[0].iloc[:, 0]
          col1 = bilancoDf[0].iloc[:, 1]
          col2 = bilancoDf[0].iloc[:, 2]
          col3 = bilancoDf[0].iloc[:, 3]
          col4 =sektor.text;
          col5 =raporlamaTuru.text;
          col6=yil.text;
          col7="Bilanco";
          bilancoTableExcel["KalemAdi"] = col_baslik;
          bilancoTableExcel[bilancoDf[0].columns[1]] = col1;
          bilancoTableExcel[bilancoDf[0].columns[2]] = col2;
          bilancoTableExcel[bilancoDf[0].columns[3]] = col3;
          bilancoTableExcel["Sektör"] = col4;
          bilancoTableExcel["Tür"] = col5;
          bilancoTableExcel["Yil"] = col6;
          bilancoTableExcel["TabloAdi"] = col7;
          print(bilancoTableExcel);
          time.sleep(1);
          # writer = pd.ExcelWriter("output.xlsx", engine='xlsxwriter')
          bilancofilename = "Bilanço"+sektor.text+"_"+raporlamaTuru.text+"_"+yil.text;
          xlWriter = pd.ExcelWriter(dir+bilancofilename + '.xlsx', engine='xlsxwriter');
          bilancoTableExcel.to_excel(xlWriter, sheet_name='Sheet{}'.format(1));
          xlWriter.save();
        except:
          print("Hata Oluştu Döngü Devam Ediyor")
          continue;

time.sleep(5);
print("Bilanço Bitti")
driver.quit();
url = "https://www.kgk.gov.tr/SektorVerileri"
driver.start_client();
driver = webdriver.Chrome()
driver.get(url)
time.sleep(15)  
yildegistir = Select(driver.find_element(By.ID, value="cmbYear"))
yilSecimi =  driver.find_element(By.ID, value="cmbYear")
yilSecimiOptions = yilSecimi.find_elements(By.TAG_NAME, "option")

raporlamaTuruDegistir = Select(driver.find_element(By.ID, value="cmbFinancialReportFrameworkType"))
raporlamaTuruSecimi =  driver.find_element(By.ID, value="cmbFinancialReportFrameworkType")
raporlamaTuruSecimiOptions = raporlamaTuruSecimi.find_elements(By.TAG_NAME, "option")

sektorDegistir = Select(driver.find_element(By.ID, value="cmbSector"))
sektorSecimi =  driver.find_element(By.ID, value="cmbSector")
sektorSecimiOptions = sektorSecimi.find_elements(By.TAG_NAME, "option")

bilancoActive= driver.find_element(By.XPATH, value="/html/body/form/div[4]/div/div[5]/div[1]/div[2]/button[1]");
driver.execute_script("arguments[0].setAttribute('class', 'list-group-item list-group-item-action financial-table-type')", bilancoActive)
gelirActive= driver.find_element(By.XPATH, value="/html/body/form/div[4]/div/div[5]/div[1]/div[2]/button[2]");
driver.execute_script("arguments[0].setAttribute('class', 'list-group-item list-group-item-action financial-table-type active')", gelirActive)   
gelirActive.click(); 
print("Gelir Başladı")  
for yil in yilSecimiOptions:
    print(yil.text);
    yildegistir.select_by_value(str(yil.text));
    time.sleep(10)
    dir = os.path.join("C:\\","Users\sabri\KGKWebScraping\Gelir\\");
    if not os.path.exists(dir):
      os.mkdir(dir)
    for raporlamaTuru in raporlamaTuruSecimiOptions:
       if(raporlamaTuru.text=="Tümü"): continue; print("Tümünü Geçti");
       elif(raporlamaTuru.text=="TFRS"): raporlamaTuruDegistir.select_by_value(str(1)); print("Tfrs");
       elif(raporlamaTuru.text=="BOBİ FRS"):raporlamaTuruDegistir.select_by_value(str(2)); print("Bobi");
       time.sleep(5)
       for sektor in sektorSecimiOptions:
        if(sektor.text=="Tümü"): continue; print("Tümünü Geçti");
        print(sektor.text);
        sektorDegistir.select_by_value(sektor.get_attribute("value"));
        time.sleep(2)
        try:
          gelirTable = driver.find_element(By.ID, "generaated_table").get_attribute("outerHTML")
          gelirDf = pd.read_html(gelirTable)
          gelirTableExcel = pd.DataFrame()
          col_baslik = gelirDf[0].iloc[:, 0]
          col1 = gelirDf[0].iloc[:, 1]
          col2 = gelirDf[0].iloc[:, 2]
          col4 =sektor.text;
          col5 =raporlamaTuru.text;
          col6=yil.text;
          col7="Gelir";
          gelirTableExcel["KalemAdi"] = col_baslik;
          gelirTableExcel[gelirDf[0].columns[1]] = col1;
          gelirTableExcel[gelirDf[0].columns[2]] = col2;
          gelirTableExcel["Sektör"] = col4;
          gelirTableExcel["Tür"] = col5;
          gelirTableExcel["Yil"] = col6;
          gelirTableExcel["TabloAdi"] = col7;
          print(gelirTableExcel);
          time.sleep(1);
          # writer = pd.ExcelWriter("output.xlsx", engine='xlsxwriter')
          gelirfilename = "Gelir"+sektor.text+"_"+raporlamaTuru.text+"_"+yil.text;
          xlWriter = pd.ExcelWriter(dir+gelirfilename + '.xlsx', engine='xlsxwriter');
          gelirTableExcel.to_excel(xlWriter, sheet_name='Sheet{}'.format(1));
          xlWriter.save();
        except:
          print("Hata Oluştu Döngü Devam Ediyor")
          continue;
print("Gelir Bitti")
driver.quit();
url = "https://www.kgk.gov.tr/SektorVerileri"
driver.start_client();
driver = webdriver.Chrome()
driver.get(url)
time.sleep(15)  
yildegistir = Select(driver.find_element(By.ID, value="cmbYear"))
yilSecimi =  driver.find_element(By.ID, value="cmbYear")
yilSecimiOptions = yilSecimi.find_elements(By.TAG_NAME, "option")

raporlamaTuruDegistir = Select(driver.find_element(By.ID, value="cmbFinancialReportFrameworkType"))
raporlamaTuruSecimi =  driver.find_element(By.ID, value="cmbFinancialReportFrameworkType")
raporlamaTuruSecimiOptions = raporlamaTuruSecimi.find_elements(By.TAG_NAME, "option")

sektorDegistir = Select(driver.find_element(By.ID, value="cmbSector"))
sektorSecimi =  driver.find_element(By.ID, value="cmbSector")
sektorSecimiOptions = sektorSecimi.find_elements(By.TAG_NAME, "option")

bilancoActive= driver.find_element(By.XPATH, value="/html/body/form/div[4]/div/div[5]/div[1]/div[2]/button[1]");
driver.execute_script("arguments[0].setAttribute('class', 'list-group-item list-group-item-action financial-table-type')", bilancoActive)
nakitakisActive= driver.find_element(By.XPATH, value="/html/body/form/div[4]/div/div[5]/div[1]/div[2]/button[3]");
driver.execute_script("arguments[0].setAttribute('class', 'list-group-item list-group-item-action financial-table-type active')", nakitakisActive)   
nakitakisActive.click();
print("Nakit Akis Basladı.")   
for yil in yilSecimiOptions:
    print(yil.text);
    yildegistir.select_by_value(str(yil.text));
    time.sleep(5)
    dir = os.path.join("C:\\","Users\sabri\KGKWebScraping\Sabri\\");
    if not os.path.exists(dir):
      os.mkdir(dir)
    for raporlamaTuru in raporlamaTuruSecimiOptions:
       if(raporlamaTuru.text=="Tümü"): continue; print("Tümünü Geçti");
       elif(raporlamaTuru.text=="TFRS"): raporlamaTuruDegistir.select_by_value(str(1)); print("Tfrs");
       elif(raporlamaTuru.text=="BOBİ FRS"):raporlamaTuruDegistir.select_by_value(str(2)); print("Bobi");
       time.sleep(5)
       for sektor in sektorSecimiOptions:
        if(sektor.text=="Tümü"): continue; print("Tümünü Geçti");
        print(sektor.text);
        sektorDegistir.select_by_value(sektor.get_attribute("value"));
        time.sleep(2)
        try:
          nakitakisTable = driver.find_element(By.ID, "generaated_table").get_attribute("outerHTML")
          nakitakisDf = pd.read_html(nakitakisTable)
          nakitakisTableExcel = pd.DataFrame()
          col_baslik = nakitakisDf[0].iloc[:, 0]
          col1 = nakitakisDf[0].iloc[:, 1]
          col4 =sektor.text;
          col5 =raporlamaTuru.text;
          col6=yil.text;
          col7="NakitAkis";
          nakitakisTableExcel["KalemAdi"] = col_baslik;
          nakitakisTableExcel[nakitakisDf[0].columns[1]] = col1;
          nakitakisTableExcel["Sektör"] = col4;
          nakitakisTableExcel["Tür"] = col5;
          nakitakisTableExcel["Yil"] = col6;
          nakitakisTableExcel["TabloAdi"] = col7;
          print(nakitakisTableExcel);
          time.sleep(1);
          # writer = pd.ExcelWriter("output.xlsx", engine='xlsxwriter')
          nakitakisfilename = "NakitAkis"+sektor.text+"_"+raporlamaTuru.text+"_"+yil.text;
          xlWriter = pd.ExcelWriter(dir+nakitakisfilename + '.xlsx', engine='xlsxwriter');
          nakitakisTableExcel.to_excel(xlWriter, sheet_name='Sheet{}'.format(1));
          xlWriter.save();
        except:
          print("Hata Oluştu Döngü Devam Ediyor")
          continue;
print("Nakit Akiş  Bitti")
print("Tüm Dosyalar Kaydedildi.")
driver.close();





# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 19:06:02 2021

@author: rkrit
"""
# Required imports
import requests
import validators
import time
import re
from bs4 import BeautifulSoup
from plyer import notification 
import traceback




# Function to validate the url provided by the user
def validate_url(user_url):
    valid=validators.url(user_url)
    return valid


# Function to get the actual text values from the html elements of the webpage
def get_actual_values(placeHolder):  
    if str(placeHolder)!="None":        
        value=placeHolder.text.strip()
        return value
    else:
        return "None"
    
def extract_price_info(parsed_doc):
            availability="None"
     # Finding the actual price
            # actual_price=parsed_doc.find('span', id='priceblock_ourprice').text.strip()     
            price=parsed_doc.find('span', id='priceblock_ourprice')
            price_val=get_actual_values(price) 
            print("ourprice--",price_val)
            
           
            # There exists a range of price values in the following case
            # Taking the least value of the range for our processing           
            if 'CDN$' in price_val and price_val.index("-")>0:
                print("Insideee")
                for i in range(0,len(price_val)):
                    split_data=price_val.split();
                    # print(i)
                    if 'CDN$'==split_data[i]:
                        lower_price="CDN$"+split_data[i+1]
                        price_val=lower_price
                        availability="In Stock."
                        print("low price",price_val)
                        break;
           
            if price_val=="None":
                sale_price=parsed_doc.find('span', id='priceblock_saleprice')
                price_val=get_actual_values(sale_price)
                
                print("sale_price---",price_val)
            
            # Checking if the price value is still empty
            if price_val=="None":
                # Finding feature price in some cases
                feat_price=parsed_doc.find('div', id='olp_feature_div')
                feature=get_actual_values(feat_price)
                
                if feature!="None":
                    feat=feature.split()
                    print(feat)
                    if 'CDN$' in feat:
                        for i in range(0,len(feat)):
                            print(i)
                            if 'CDN$'==feat[i]:
                                feature_price="CDN$"+feat[i+1]
                                price_val=feature_price
                                availability="In Stock."
                                break;
                                
                    print("feature price---",feature_price)
                    if feature_price=="None":
                        # price_val="Sorry, not able to fetch the price for the chosen product" 
                         price_val=False
                        
            else:
                availability="In Stock."
                  
            return price_val,availability; 

def handle_stock_check():
     message="Yay! The product has come back in stock now. Check the website"
     print(message)
     return message
        

def handle_price_check():   
    message="Hurray!! The price of the product has gone down. Check website for more details"
    print(message)
    return message


# Extracting information from page
def extract_pageInfo(url,option,current_price):
    
    # Defining headers
    headers = {
    'content-type': 'text/html;charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',


    # from lxml.html import fromstring
    # def get_proxies():
    #     url = 'https://free-proxy-list.net/'
    #     response = requests.get(url)
    #     parser = fromstring(response.text)
    #     print("eeeee",parser)
    #     proxies = set()
    #     for i in parser.xpath('//tbody/tr')[:10]:
    #         if i.xpath('.//td[7][contains(text(),"yes")]'):
    #             #Grabbing IP and corresponding PORT
    #             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
    #             proxies.add(proxy)
    #     return proxies
    
    
    # proxy = get_proxies()
    # print(proxy)
     
    # Fetching the content from the url
    try:
        
       

        send_header = {
               'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0',
               'referer': 'http://www.bing.com/'
              }
        send_proxies = {'http':'0.0.0.0:80','https':'0.0.0.0:80'}
        # url = 'https://www.azlyrics.com/lyrics/taylorswift/dropsofjupiter.html'
        
        
        
        
        
        
        
        
        
        
        
        
        
        
   
        response = requests.get(url, headers=headers,proxies = send_proxies) 
       
        if response.status_code == response.codes.ok:
          print('Everyhing Is Working...')
        
        # Parsing the html content 
        parsed_doc = BeautifulSoup(response.content, 'lxml')
        
        # Recording the product title
        prodTitle=parsed_doc.find('span', id='productTitle')
        title=get_actual_values(prodTitle)  
        
        # print('title- -',title)       
        
        
        
        # Finding the availability of the product
        availability=parsed_doc.find('div', id='availability')
        availability_value=get_actual_values(availability)               
      
        
        # Handling other cases of shipping status  
        if "ships" in str(availability_value):           
            availability_value="In Stock."
        
        # In some cases the availability is not explicity mnetioned, so getting it from the price field in the website    # 
        
        # Get the product price
        prod_price,availability_value=extract_price_info(parsed_doc)
        # value = ''.join(x for x in prod_price if x.isdigit())
        # print("prod_price here",value)
      
        # if(int(value)>0):
        #     availability_value!="In Stock."
                
        print("availability***---",availability_value)        
                
        # Handling out of stock scenario 
        if(availability_value!="In Stock."):  
            
            if(str(availability_value)=="None"):
                result="Error fetching information about product availability. Trying again in a few minutes.."
                print(result)               
            elif(re.sub(r"\s+", "", availability_value)!=""):               
                avail=availability_value.split()
                print("avail***",avail)
                # print(avail[0]+" "+avail[1])
                if (avail[0]+" "+avail[1])=="Currently unavailable.":
                    print("Looks like the product is still out of Stock. Trying again....")                
                else:
                    print("Error fetching information about product availability.Trying again in a few minutes..")  
                      
       
        message=""
       
       
        if(option==1 and availability_value=="In Stock." ):            
            message=handle_stock_check()      
        
        if(option==2):  
            print("option 2 ",prod_price)
            value=prod_price.split("$",1)
            print("vallll",value)
            # value = ''.join(x for x in prod_price if x.isdigit() and x==".")
            
            # if(int(value)<current_price):                  
            #     message=handle_price_check()      
          
        format_notifier_message(option,message,title);
       
                            
                        
        
    except Exception as e:
    #if the data is not fetched due to lack of internet
        print(e)
        print(traceback.format_exc())
        print("ERROR: Cannot fetch data from the website. Trying again in a few minutes")  
    
    
        
            




def extract_url(url):

    if url.find("www.amazon.ca") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.ca" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.ca" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url



def format_notifier_message(choice,message,title):
    if len(title) > 30:
        info = (title[:30] + '..') 
    else:
        info=title
    notification.notify(
        
        title = "Amazon Product - "+info,
        #the body of the notification
        message = message,  
       
        # Icon for notification
        app_icon = "Paomedia-Small-N-Flat-Bell.ico",
       
        timeout  = 1
    )
       




# Testing  


# # Getting details from the user
# user_url=input("Please enter the Amazon URL for the product that you're looking for: \n" )
# while 1:
#     if not(validate_url(user_url)):
#         user_url=input("Please enter a valid URL")
#     else:
#         break;

# current_price=1000000  
# while 1:
#     option=int(input("Choose either one of the following options \n 1. Product Stock check \n 2. Product Price check \n \n" ))
#     if(option==1):
#         print("You will be notified about the product status every 5 minutes")
#         break;
#     elif(option==2):
#         current_price=float(input("Enter the current price of the product in CAD: "))
#         print("You will be notified if there is a change in the product price")
#         break;
#     else:
#         print("Please choose a valid option")




# url='https://www.amazon.ca/Disposable-Designs-Face_Masks-Disposable_Masks-Protection/dp/B08ZY96BQW/ref=sr_1_7?dchild=1&keywords=out+of+stock&qid=1619459587&refinements=p_n_availability%3A12035748011&rnid=5264023011&s=industrial&sr=1-7'

# Sample Input URL's

# works - in stock
# url = 'https://www.amazon.ca/INIU-High-Speed-Flashlight-Powerbank-Compatible/dp/B07CZDXDG8'
# url='https://www.amazon.ca/Better-Sense-Hoola-Hoop-Adults/dp/B08GQ9QHGD/ref=sr_1_171?dchild=1&qid=1619462204&refinements=p_n_availability%3A12035748011&rnid=12035746011&s=sports&sr=1-171'



# url='https://www.amazon.ca/52-5-Adjustable-Cast-Iron-Dumbbell/dp/B009GC76QO/ref=sr_1_187?dchild=1&qid=1619465251&refinements=p_n_availability%3A12035748011&rnid=12035746011&s=sports&sr=1-187'



# feature price
# nw
# url='https://www.amazon.ca/dp/B07DHZ7ZHH/ref=s9_acsd_omwf_hd_bw_b2cpsqp_c2_x_0_i?pf_rd_m=A1IM4EOPHS76S7&pf_rd_s=merchandised-search-11&pf_rd_r=FKSXABMQVPH1M42T1EXF&pf_rd_t=101&pf_rd_p=7b0bd099-bb9c-59f9-a90a-9cc97790b45c&pf_rd_i=2406132011'
# url='https://www.amazon.ca/HoMedics-AP-P20-Light-Personal-Sanitizer/dp/B085PSQ5JW/ref=sr_1_177?dchild=1&keywords=sanitizer&qid=1619460165&refinements=p_n_availability%3A12035748011&rnid=12035746011&sr=8-177'

# url='https://www.amazon.ca/AUKEY-Mechanical-Customizable-Anti-Ghosting-Multimedia/dp/B086SVN194?ref_=Oct_s9_apbd_omwf_hd_bw_b7jmMSJ&pf_rd_r=FYJCCJKMM4X7VFG3CY0H&pf_rd_p=0a2d1443-7ca7-54f3-b0b0-a7fa48318cf0&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=7089391011'

# out of stock items
# url='https://www.amazon.ca/Disposable-Designs-Face_Masks-Disposable_Masks-Protection/dp/B08ZY96BQW/ref=sr_1_7?dchild=1&keywords=out+of+stock&qid=1619459587&refinements=p_n_availability%3A12035748011&rnid=5264023011&s=industrial&sr=1-7'
# url='https://www.amazon.ca/Antibacterial-Instant-Sanitizing-Premium-Commercial/dp/B08G9MXWRM/ref=sr_1_15?dchild=1&keywords=sanitizer&qid=1619459932&refinements=p_n_availability%3A12035748011&rnid=12035746011&sr=8-15'

    
# url="https://www.amazon.ca/PHYTOFAB-Hand-Sanitizer-Moisturizing-Gel/dp/B08L9QG7DF/ref=pd_di_sccai_5?pd_rd_w=BqgsD&pf_rd_p=e92f388e-b766-4f7f-aac1-ee1d0056e8fb&pf_rd_r=4C5A2FE08P7RKTB974RH&pd_rd_r=1f35bf42-fc24-491c-9360-0ad17443bb63&pd_rd_wg=dE1ed&pd_rd_i=B08L9QG7DF&psc=1"

# range of values
# url="https://www.amazon.ca/dp/B01M1DKMHP/ref=s9_acsd_otopr_hd_bw_bBEcDRj_c2_x_0_i?pf_rd_m=A1IM4EOPHS76S7&pf_rd_s=merchandised-search-11&pf_rd_r=A0D2V5S7NN9DV52XSB5N&pf_rd_t=101&pf_rd_p=e84a1b60-69c9-54a0-848d-804d206dca2a&pf_rd_i=10293438011"


# url="https://www.amazon.ca/dp/B086MBQKH2/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B086MBQKH2p13NParams&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE2UUhQWU85WjBQTFcmZW5jcnlwdGVkSWQ9QTEwMTk5MzEyRERFUFUwUENUTzhVJmVuY3J5cHRlZEFkSWQ9QTA2MjEzMTczTzRNN09HRUcyU09WJndpZGdldE5hbWU9c3BfZGV0YWlsMiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="
# url="https://www.amazon.ca/SONGMICS-Customizable-Display-Bathroom-Shelving/dp/B07FKHS5SN?ref_=Oct_s9_apbd_omwf_hd_bw_b6pSF0d&pf_rd_r=YR13KRQ3EGHZH8MMYW33&pf_rd_p=39fb29bf-a517-5d91-ab3f-7bef0b019d28&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=6257121011"

# url="https://www.amazon.ca/SONGMICS-Customizable-Display-Bathroom-Shelving/dp/B07FKHS5SN?ref_=Oct_s9_apbd_omwf_hd_bw_b6pSF0d&pf_rd_r=YR13KRQ3EGHZH8MMYW33&pf_rd_p=39fb29bf-a517-5d91-ab3f-7bef0b019d28&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=6257121011"
url="https://www.amazon.ca/Likesuns-Dual-Head-Spectrum-Adjustable-Gooseneck/dp/B084YXDS1B/ref=bmx_2?pd_rd_w=6VK7w&pf_rd_p=d9347c84-a27a-4c22-b959-7bb71382273b&pf_rd_r=DA853TBWFNXWCTMSCS2G&pd_rd_r=5ffeca70-bf35-4685-8c8f-9d09bfc9bcdd&pd_rd_wg=4zb4U&pd_rd_i=B084YXDS1B&psc=1"
url=extract_url(url)
print("Trying to reach the url --",url)
option=2
current_price=0
while(True):
    extract_pageInfo(url,option,current_price) 
    #notification repeats after every 4hrs
    #time.sleep(60*60*4)
    time.sleep(5)  





# works - in stock
# url='https://www.amazon.ca/Better-Sense-Hoola-Hoop-Adults/dp/B08GQ9QHGD/ref=sr_1_171?dchild=1&qid=1619462204&refinements=p_n_availability%3A12035748011&rnid=12035746011&s=sports&sr=1-171'
# Sample Input URL's


# url='https://www.amazon.ca/52-5-Adjustable-Cast-Iron-Dumbbell/dp/B009GC76QO/ref=sr_1_187?dchild=1&qid=1619465251&refinements=p_n_availability%3A12035748011&rnid=12035746011&s=sports&sr=1-187'


# url='https://www.amazon.ca/dp/B07DHZ7ZHH/ref=s9_acsd_omwf_hd_bw_b2cpsqp_c2_x_0_i?pf_rd_m=A1IM4EOPHS76S7&pf_rd_s=merchandised-search-11&pf_rd_r=FKSXABMQVPH1M42T1EXF&pf_rd_t=101&pf_rd_p=7b0bd099-bb9c-59f9-a90a-9cc97790b45c&pf_rd_i=2406132011'

# feature price
# url='https://www.amazon.ca/HoMedics-AP-P20-Light-Personal-Sanitizer/dp/B085PSQ5JW/ref=sr_1_177?dchild=1&keywords=sanitizer&qid=1619460165&refinements=p_n_availability%3A12035748011&rnid=12035746011&sr=8-177'
# url='https://www.amazon.ca/AUKEY-Mechanical-Customizable-Anti-Ghosting-Multimedia/dp/B086SVN194?ref_=Oct_s9_apbd_omwf_hd_bw_b7jmMSJ&pf_rd_r=FYJCCJKMM4X7VFG3CY0H&pf_rd_p=0a2d1443-7ca7-54f3-b0b0-a7fa48318cf0&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=7089391011'

# out of stock items
# url='https://www.amazon.ca/Disposable-Designs-Face_Masks-Disposable_Masks-Protection/dp/B08ZY96BQW/ref=sr_1_7?dchild=1&keywords=out+of+stock&qid=1619459587&refinements=p_n_availability%3A12035748011&rnid=5264023011&s=industrial&sr=1-7'
# url='https://www.amazon.ca/Antibacterial-Instant-Sanitizing-Premium-Commercial/dp/B08G9MXWRM/ref=sr_1_15?dchild=1&keywords=sanitizer&qid=1619459932&refinements=p_n_availability%3A12035748011&rnid=12035746011&sr=8-15'

    





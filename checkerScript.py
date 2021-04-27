# -*- coding: utf-8 -*-
"""
@author: Krithiga Subramaniam Ravichandran
@StudentNo: 101204303
E-commerce Availability checker

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
            
            # Finding the actual price of the product           
            price=parsed_doc.find('span', id='priceblock_ourprice')
            price_val=get_actual_values(price)        
            
           
            # There exists a range of price values in the following case
            # Taking the least value of the range for our processing  
            price_interval=False
            if price_val.find("-")>-1:
                price_interval=True
            if 'CDN$' in price_val and price_interval  :
               
                for i in range(0,len(price_val)):
                    split_data=price_val.split();
                   
                    if 'CDN$'==split_data[i]:
                        lower_price="CDN$"+split_data[i+1]
                        price_val=lower_price
                        availability="In Stock."                       
                        break;
           
            if price_val=="None":
                sale_price=parsed_doc.find('span', id='priceblock_saleprice')
                price_val=get_actual_values(sale_price)                
              
            
            # Checking if the price value is still empty
            if price_val=="None":
                # Finding feature price in some cases
                feat_price=parsed_doc.find('div', id='olp_feature_div')
                feature=get_actual_values(feat_price)
                
                feature_price=""
                if feature!="None":
                    feat=feature.split()                   
                    if 'CDN$' in feat:
                        for i in range(0,len(feat)):                          
                            if 'CDN$'==feat[i]:
                                feature_price="CDN$"+feat[i+1]
                                price_val=feature_price
                                availability="In Stock."
                                break;                                
                   
                    if feature_price=="None":
                        # Not able to fetch the price for the chosen product
                         price_val=False
                        
            else:
                availability="In Stock."
                  
            return price_val,availability; 

def handle_stock_check():
     message="Yay! The product is back in stock now. Check the website"
     print(message)
     return message
        

def handle_price_check():   
    message="Hurray!! The price of the product has reduced. Check website for more details"
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
    
     
    # Fetching the content from the url
    try:
        response = requests.get(url, headers=headers)       
      
        
        # Parsing the html content 
        parsed_doc = BeautifulSoup(response.content, 'lxml')
        
        # Recording the product title
        prodTitle=parsed_doc.find('span', id='productTitle')
        title=get_actual_values(prodTitle)  
        
        # Finding the availability of the product
        availability=parsed_doc.find('div', id='availability')
        availability_value=get_actual_values(availability)               
      
        
        # Handling other cases of shipping status  
        if "ships" in str(availability_value):           
            availability_value="In Stock."
        
        # In some cases the availability is not explicity mnetioned, so getting it from the price field in the website    # 
        
        # Get the product price and availability
        prod_price,availability_value=extract_price_info(parsed_doc)      
                
            
                
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
            value=prod_price.split("$",1)          
            int_val=value[1].strip()          
            if(float(int_val)<current_price):                  
                message=handle_price_check()      
          
        format_notifier_message(option,message,title);  
        
    except Exception as e:
        #if the data is not fetched due to any issues
        print(e)
        # print(traceback.format_exc())
        print("ERROR: Cannot fetch data from the website. Trying again in a few minutes")  

# Extracting the url from the user given value
def shorten_url(url):

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


# Formatting the messages for the notifier
def format_notifier_message(choice,message,title):
    if len(title) > 30:
        info = (title[:30] + '..') 
    else:
        info=title
    notification.notify(
        
        title = "Amazon Product - "+info,       
        message = message,  
       
        # Loading Icon for notification
        app_icon = "Paomedia-Small-N-Flat-Bell.ico",       
        timeout  = 10
    )
       




# Testing  


# Getting details from the user
user_url=input("Please enter the Amazon URL for the product that you're looking for: \n" )
while 1:
    if not(validate_url(user_url)):
        user_url=input("Please enter a valid URL")
    else:
        break;

current_price=0  
while 1:
    option=int(input("Choose either one of the following options \n 1. Product Stock check \n 2. Product Price check \n \n" ))
    if(option==1):
        print("You will be notified about the product status every 2 hours.")
        break;
    elif(option==2):
        current_price=float(input("Enter the current price of the product in CAD: "))
        print("You will be notified if there is a change in the product price.")
        break;
    else:
        print("Please choose a valid option")




url=shorten_url(user_url)
print("Trying to reach the url --",url)

while(True):
    extract_pageInfo(url,option,current_price) 
    #notification repeats for every 2hrs
    time.sleep(60*60*2)

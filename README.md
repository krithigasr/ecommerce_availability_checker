# E-commerce Product Availability Checker

<div align="right">
- Krithiga Subramaniam Ravichandran
(101204303)
</div>
<style>body {text-align: justify}</style>
## Contents
* Problem Statement
* Prerequisites 
* Running the Python Script
* Testing- Input examples
* Output
* Code Design
* Impact
* Challenges
* Future improvements
* References

## Problem Statement

With the growth of E-commerce, shopping for all commodities have been shifted online and can happen within the comfort of our homes. Often, there are scenarios where we would be interested in a product and it might have gone out of stock or even worse, may not be at an affordable price. One might even look for some ’grab the deal’ offers. All this leads to us having to regularly check for the product to get back in stock or get listed at a reduced price. And if we are not lucky enough, the product would go out of stock again quickly. To address this problem effectively, I have developed  a  Python script that keeps monitoring the product and informs the availability and/or reduced price  to the user through desktop notifications. For the purpose of this project, I have made use of Amazon website as it is one of the largest e-commerce platforms in the world.

## Prerequisites 

* This code is partially platform specific. While the code to fetch and process product information is independent of any platform, the module used for sending desktop notifications _only works_ on Windows.   

* You need  a IDE to effectively make use of this script, I used the Spyder IDE to develop my code. You may install it using the Anaconda toolkit  link given below.

	[Anaconda](https://www.anaconda.com/products/individual)

* To download the project, follow the steps below,

    * Install Git (The 'User' can use Git bash or any other software of choice to clone the project).

    * Create a new folder for the project. Right-click inside the folder and open gitbash.

    * Type the following command in the git terminal: 
    ```
    git clone https://github.com/krithigasr/ecommerce_availability_checker 
    ```
    
    
    OR 

    Go to [E-commerce availability checker](https://github.com/krithigasr/ecommerce_availability_checker) and click on "Download" option to download the zip folder of the project.

* You will also need to install the following libraries to make the code work. If using Anaconda, open the anaconda prompt and install the following using the command,
    ```
    pip install <library_name>
    ```
    The libraries needed are -  requests, validators, time, re, bs4, plyer and  traceback.

## Running the Python Script 

* In the IDE that you are using, open the file 'checkerScript.py' from the git repository you downloaded.
* Make sure all the imports are properly downloaded, otherwise you might be faced with errors in the console. Fix those errors and retry.

## Testing

* On successful execution of the script, you will be faced with the following output in the screen. 

    ![image](https://user-images.githubusercontent.com/42897174/116188778-f7d40e00-a6f5-11eb-834b-2fbbea30930f.png)


* First, enter the amazon product URL which you would like to process. This can be directly copied from the address bar of your browser. Please choose the product link from **Amazon Canada** as the code has been developed keeping in mind the structure of that particular website.
* If the URL you entered is invalid, you will be prompted to enter a right one.
* After giving the URL, you have to select either  _Product Stock check_ or _Product Price check_.
* These are some of the sample URL's that you could use to play around with the script-

	 [URL 1](https://www.amazon.ca/HoMedics-AP-P20-Light-Personal-Sanitizer/dp/B085PSQ5JW/ref=sr_1_177?dchild=1&keywords=sanitizer&qid=1619460165&refinements=p_n_availability%3A12035748011&rnid=12035746011&sr=8-177),[URL 2](https://www.amazon.ca/dp/B01M1DKMHP/ref=s9_acsd_otopr_hd_bw_bBEcDRj_c2_x_0_i?pf_rd_m=A1IM4EOPHS76S7&pf_rd_s=merchandised-search-11&pf_rd_r=A0D2V5S7NN9DV52XSB5N&pf_rd_t=101&pf_rd_p=e84a1b60-69c9-54a0-848d-804d206dca2a&pf_rd_i=10293438011),	[URL 3](https://www.amazon.ca/AUKEY-Mechanical-Customizable-Anti-Ghosting-Multimedia/dp/B086SVN194?ref_=Oct_s9_apbd_omwf_hd_bw_b7jmMSJ&pf_rd_r=FYJCCJKMM4X7VFG3CY0H&pf_rd_p=0a2d1443-7ca7-54f3-b0b0-a7fa48318cf0&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=7089391011).
	
* Now, the script will start running and you will be notified if there is a change in the product availability status or in the price of the product. The code is executed every two hours.

* To stop the script from running, you can kill it either from the IDE or use the Task manager to kill the corresponding process.

## Output
* First let's test the **Product Stock Checker** feature of the script. I'm giving a product that is in stock, in order to verify if this function works. Because, if a product that is out of stock is given we wouldn't know when we will receive the notification.
    * Choose option 1 after entering a sample URL. The screenshots are attached below,
    
        ![image](https://user-images.githubusercontent.com/42897174/116188820-03bfd000-a6f6-11eb-80d8-7b63e411c27b.png)
    * This is the kind of notification we will receive after the product is back in stock,
      
        ![image](https://user-images.githubusercontent.com/42897174/116188946-37025f00-a6f6-11eb-93e3-e023c998b780.png)

 * Now let's test the **Product Price Checker** feature of the script. We choose option 2 after entering the URL of the product. For the purpose of testing, I'm giving the current price of the product to be higher than what it is in order to make sure that this module indeed works.
    * Screenshot showing the entered option and current price of the product below,

        ![image](https://user-images.githubusercontent.com/42897174/116188984-44b7e480-a6f6-11eb-81b3-b469396608b5.png)
    
    * This shows the notification we receive after a price drop happens,
    
        ![image](https://user-images.githubusercontent.com/42897174/116188999-4a152f00-a6f6-11eb-93d3-372dc6bc1dcb.png)

## Customizing the script
* For now, the code has been written in such a way that the script is run every 2 hours. You may  modify this according to your needs.
* To change the time, please modify the following line of code in the script.
        ![image](https://user-images.githubusercontent.com/42897174/116188905-2651e900-a6f6-11eb-8edf-dbd05c8d893c.png)
*  For example, if you wish to run the code every one hour, you would simply change this as follows,

    ![image](https://user-images.githubusercontent.com/42897174/116190101-03283900-a6f8-11eb-9a6a-1b291b21c9b7.png)

  

## Code Design
The code has been developed keeping in mind the dynamics of the content in the Amazon Canada website. I have split the code into small functions based on their functionality and also to keep the code understandable.

### User Input
* First, the url and the Product stock or price checker option is recorded from the user. 
* The url is validated and then if the price checker option is chosen, the current price of the product is received as input.

### Loading content from the website
* Based on the url provided, we try to load the contents of the webpage by setting the headers and using the requests module . 
* We make use 'Beautiful Soup' module to parse the html content.  Essentially, a _Web Scraping_ approach is used to get the title, availability and price of the required product.
* The id's of each element is used according to the structure of the website and the values are populated.

### Processing the data
* Depending on the option chosen, we process the availability and the price of the product and send a notification when either of these values change.
* If we are not able to find the availability/price due to connectivity issues or other errors, corresponding message is displayed on the console and the script tries again after the specified sleep time.

### Notifying the user
* We use the _Notifications_ module to send a  desktop notification to the user when the product information changes. 
* This module is developed exclusively for Windows. If you're using Mac/Linux OS then be sure to comment the code related to notification.

### Execution frequency of the script
* As mentioned already, the script runs for every 2 hours and this can be modified by changing the sleep time of the notifier.


## Impact 
 With the help of this script we will eliminate manual work that needs to be done to continuously check the product site to see if the product that we need has come back in stock or has reduced in price. Also, this will be a useful piece of code during this pandemic as all our shopping has moved to the online platform. Due to the increased demand, we always come across products that go out of stock. In such scenarios, we can make use of the script to keep running in the background while we perform our other tasks. During Black Friday or other sales where there are deals on products we can use this script instead of having to monitor the price of the product regularly.

## Challenges
I came across few challenges in the course of developing this project. One of the major challenge was to fetch the contents of the product. I first tried to recover the details using the open ended API's of the e-commerce websites but I was not able to get the API key and password. So, I used web scraping technique to get the required product details. Owing to this, I wasn't able to make the script generic and stuck only with Amazon website for the scope of this project.

Another drawback using web scraping was the way in which we fetch the product availability and price had to customized in accordance to how the website displayed information for that particular part. I identified three themes - Two for products in stock and one for out of stock products and have coded similarly to fetch the relevant details. For the former, there were two ways in which prices were display, sometimes just a single value as we would normally expect and rarely as a range. The code takes in account of all these formats. This was one more reason why it couldn't be extended to other websites even with the web scraping technique. 

Other point to take note is that these websites are capable of web scraping activities and they will block our IP address if the same script(with the same parameters) are run multiple times within short intervals.


## Future improvements
Like mentioned in the previous section, the initial goal was to develop a generic script that can cater to fetching product specific information. But due to the problems in getting the API key and password, this could not be done. In the future, I would want to makes changes in the script by fetching information with open ended API's as that provides reliable data. Web scraping is not very dependable as the website structure can change anytime. Also, an email notification to the user will be a good addition to this script.

We can also add additional modules that offers comparable prices in other websites based on the product given by the user. Price/Availability monitoring can also be made available on a multitude of e-commerce sites.


## References

*  ”US  ecommerce  grows  44.0%  in  2020  —  Digital  Commerce  360”,  Digital  Commerce  360,  2021.  [Online].  Available:  www.digitalcommerce360.com/article/us-ecommerce-sales/
* P.Smyth,”CreatingWebAPIswithPythonandFlask”,Programminghistorian.org,2021.[Online].Available:https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
*  ”Create Price Alerts For Amazon Products”, Medium, 2021. [Online]. Available: https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
*  ”Desktop notifications with Python”,[Online].Available: https://towardsdatascience.com/create-desktop-notifier-application-using-python-fb3b7b2c3cf3
*  ”A Single Line of Python Code Scraping Dataset from Webpages”, Medium, 2021. [Online]. Available: https://towardsdatascience.com/a-single-line-of-python-code-scraping-dataset-from-webpages-c9d2a8805d61
* ”Tutorial: Amazon price tracker using Python and MongoDB (Part 1)”, Medium, 2021. [Online]. Available: https://medium.com/analytics-vidhya/tutorial-amazon-price-tracker-using-python-and-mongodb-part-1-aece6347ec63
* ”How to Scrape Walmart Reviews using Python-Walmartreviewscraper”,WorthWebScraping,2021.[Online].Available:https://www.worthwebscraping.com/how-to-scrape-walmart-reviews-using-python/


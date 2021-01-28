# GCP Batch Processing

## Building a pipeline for batch processing scrapped web data into cloud storage and big query

Scraping Booking.com hotel searches  by building on some existing work ad implementing a scraper in `scraper.py`: 
https://github.com/ZoranPandovski/BookingScraper
https://www.scrapehero.com/scrape-property-data-from-booking-com-using-google-chrome/


a) bookingsscrapper generates HTTP end point and gets triggered to run the scraper and store it as csv in tmp dir in the cloud vm and then 
uploads the data into google cloud storage bucket.
/

<img width="825" alt="Screenshot 2021-01-27 at 23 24 49" src="https://user-images.githubusercontent.com/16509490/106072239-bab0ad80-60ff-11eb-8430-ea242bc7362a.png">


b) I initially hadn't checked the output of the scraper closely enough and only later realised that there was some further cleaning required to get the data i need in the right format. I did not want to go back and write more scripts so decided to use dataprep for the ETL, which has a nice flexible easy to use interactive interface for producing a cleaning recipe as part of a dataflow job.  This was setup to clean the raw data landing from a) in the cloud bucket and uploading to another bucket. This can be setup as schedule or another cloud function to trigger when listening to bucket event. 

<p float="left">
 <img width="814" height="400" alt="Screenshot 2021-01-28 at 00 02 54" src="https://user-images.githubusercontent.com/16509490/106072297-d451f500-60ff-11eb-91b7-f8eb11252cb7.png">
<img width="836" height="400" alt="Screenshot 2021-01-28 at 00 03 52" src="https://user-images.githubusercontent.com/16509490/106072256-c0a68e80-60ff-11eb-839d-601366b59e84.png">
</p>

c) load_bookings_from_bucket which has Bucket trigger and uploads data into bigquery when new data lands in cloud storage bucket 


<img width="835" alt="Screenshot 2021-01-27 at 23 10 50" src="https://user-images.githubusercontent.com/16509490/106072293-d1570480-60ff-11eb-93f4-6d84b215d055.png">


Can then filter data in bigquery or do further analysis in google cloud studio or merge with other source data e.g. restaurant visits from tripadvisor to give Quick query below shows cheapest hotels under under $500 for an adult on an 8 day stay from end Jan to fist week of Feb 2021.


<img width="840" alt="Screenshot 2021-01-28 at 00 15 33" src="https://user-images.githubusercontent.com/16509490/106072247-bedccb00-60ff-11eb-9035-a0a3fb2a68b4.png">



### Cloud Function setup

`main.py` contains all google cloud function scripts 

Note that cloud functions have a max timeout limit of 9 minutes althout default setting is 60 secs, and i had to increase this to avoid timing out, especially when increasing the number of pages I was making calls from. The following environment variable were set by default which  correspond to search parameters which can be changed before triggering.


<p float="left">
<img width="366" alt="Screenshot 2021-01-27 at 23 26 01" src="https://user-images.githubusercontent.com/16509490/106072249-bf756180-60ff-11eb-97f3-151997108ace.png">
<img width="384" alt="Screenshot 2021-01-27 at 23 28 14" src="https://user-images.githubusercontent.com/16509490/106072255-c00df800-60ff-11eb-8f80-e4d80d64d621.png">
</p>


Any changes to source code - requires cloud function to be deployed before triggering, for the changes to take effect. I used google source repositories and synced github with it as I was deploying locally. Important to note that the 'directory for source code' must be set to root `/`if `main.py` is in root.
the entry point must be set the same as cloud function defined in the script.


<img width="829" alt="Screenshot 2021-01-27 at 23 26 41" src="https://user-images.githubusercontent.com/16509490/106072250-bf756180-60ff-11eb-9f5f-6d85948d9cb5.png">


## Calling CLoud Natural Language API to generate sentiment for text

Tweets generated by tweepy were already streamed into Bigquery via pubsub. Cloud function `senti` in `main.py`
calls the Cloud Natural Language API, using their pre-trained model to generate sentiment for each tweet passed.
 https://cloud.google.com/natural-language/docs/sentiment-tutorial is a good tutorial which describes how to do this for text in cloud storage or single string, the code was adjusted to query the big query table containing tweets, and then iterating over each row and calling the API to generate the sentiment and packing these in json which is loaded into newly create bigquery table (after deleting exisitng one, if already exists). 
 

<img width="935" alt="Screenshot 2021-01-27 at 23 10 50" src="https://user-images.githubusercontent.com/16509490/106072293-d1570480-60ff-11eb-93f4-6d84b215d055.png">


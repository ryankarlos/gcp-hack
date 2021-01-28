# GCP Batch Processing

* Building a pipeline for batch processing scrapped web data into cloud storage and big query

Scraping Booking.com hotel searches  by building on some existing work ad implementing a scraper in `scraper.py`: 
https://github.com/ZoranPandovski/BookingScraper
https://www.scrapehero.com/scrape-property-data-from-booking-com-using-google-chrome/

a) bookingsscrapper generates HTTP end point and gets triggered to run the scraper and store it as csv in tmp dir in the cloud vm and then 
uploads the data into google cloud storage bucket.
<img width="825" alt="Screenshot 2021-01-27 at 23 24 49" src="https://user-images.githubusercontent.com/16509490/106072239-bab0ad80-60ff-11eb-8430-ea242bc7362a.png">

b) dataprep dataflow job which cleans the raw data landing from a) in the cloud bucket and uploads to another bucket. This can be setup as schedule
or another cloud function to trigger when listening to bucket event.

<p float="left">
 <img width="414" alt="Screenshot 2021-01-28 at 00 02 54" src="https://user-images.githubusercontent.com/16509490/106072297-d451f500-60ff-11eb-91b7-f8eb11252cb7.png">
<img width="436" alt="Screenshot 2021-01-28 at 00 03 52" src="https://user-images.githubusercontent.com/16509490/106072256-c0a68e80-60ff-11eb-839d-601366b59e84.png">
</p>

c) load_bookings_from_bucket which has Bucket trigger and uploads data into bigquery when new data lands in cloud storage bucket 

<img width="835" alt="Screenshot 2021-01-27 at 23 10 50" src="https://user-images.githubusercontent.com/16509490/106072293-d1570480-60ff-11eb-93f4-6d84b215d055.png">

`main.py` contains all google cloud function scripts 

Note that cloud functions have a max timeout limit of 9 minutes althout default setting is 60 secs, and i had to increase this to avoid timing out, especially when increasing the number of pages I was making calls from. The following environment variable were set by default which  correspond to search parameters which can be changed before triggering.

<p float="left">
<img width="366" alt="Screenshot 2021-01-27 at 23 26 01" src="https://user-images.githubusercontent.com/16509490/106072249-bf756180-60ff-11eb-97f3-151997108ace.png">
<img width="384" alt="Screenshot 2021-01-27 at 23 28 14" src="https://user-images.githubusercontent.com/16509490/106072255-c00df800-60ff-11eb-8f80-e4d80d64d621.png">
</p>

Any changes to source code - requires cloud function to be deployed before triggering, for the changes to take effect. 

<img width="1429" alt="Screenshot 2021-01-27 at 23 26 41" src="https://user-images.githubusercontent.com/16509490/106072250-bf756180-60ff-11eb-9f5f-6d85948d9cb5.png">
<img width="1428" alt="Screenshot 2021-01-27 at 23 27 23" src="https://user-images.githubusercontent.com/16509490/106072253-c00df800-60ff-11eb-921d-844c25ada9f6.png">

Filtering data in bigquery to give cheapest hotels under under $500 for an adult on an 8 day stay from end Jan to fist week of Feb 2021.

<img width="940" alt="Screenshot 2021-01-28 at 00 15 33" src="https://user-images.githubusercontent.com/16509490/106072247-bedccb00-60ff-11eb-9035-a0a3fb2a68b4.png">

* Calling CLoud Natural Language API to generate sentiment for text

Tweets generated by tweepy were already streamed into Bigquery via pubsub. Cloud function `senti` in `main.py`
generates
Using https://cloud.google.com/natural-language/docs/sentiment-tutorial as a baseline, the code was adjusted to
create bigquery table (after deleting exisitng one, if already exists). 

<img width="835" alt="Screenshot 2021-01-27 at 23 10 50" src="https://user-images.githubusercontent.com/16509490/106072293-d1570480-60ff-11eb-93f4-6d84b215d055.png">


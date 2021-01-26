def hello_world(request):

    import csv
    from scraper import scrape, create_url
    import os
    import datetime
    from gcloud import storage

    max_search = os.environ("MAX_SEARCH")
    people = os.environ("PEOPLE")
    city = [
        "London",
        "bristol",
        "cornwall",
        "brighton",
        "portsmouth",
        "bournemouth",
        "manchester",
        "yorkshire",
        "gloucestershire",
    ]
    checkin_date = datetime.datetime.now() + datetime.timedelta(os.environ("CHECKIN"))
    checkout_date = checkin_date + datetime.timedelta(os.environ("CHECKOUT"))

    with open("data.csv", "w") as outfile:
        fieldnames = [
            "name",
            "location",
            "price",
            "price_for",
            "room_type",
            "beds",
            "rating",
            "rating_title",
            "number_of_ratings",
        ]
        urllist = []
        for c in city:
            urllist.extend(
                create_url(people, c, checkin_date, checkout_date, max_search)
            )

        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for url in urllist:
            data = scrape(url)
            if data:
                try:
                    for h in data["hotels"]:
                        writer.writerow(h)
                except:
                    print("Skipping to next as offset exceeds max search")
                # sleep(5)

        client = storage.Client()
        bucket = client.get_bucket('scraping')
        blob = bucket.blob('booking.csv')
        blob.upload_from_filename('data.csv')

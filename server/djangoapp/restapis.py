import requests
import json
import configparser
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
import Features, SentimentOptions
from .models import CarDealer, DealerReview  # import related models here
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    
    response = None
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    #try:
    response = requests.post(url, json=json_payload, params=kwargs)
    #except:
       # print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id = kwargs['id'])
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_reviews = json_result
        # For each dealer object
        for dealer_review in dealer_reviews:
            # Get its content in `doc` object
            # Create a DealerReview object with values in `doc` object
            sentiment = analyze_review_sentiments(dealer_review['review'])
            reviews_obj = DealerReview(dealership=dealer_review["dealership"], name=dealer_review["name"], purchase=dealer_review["purchase"],
                                   id=dealer_review["id"], review=dealer_review["review"], purchase_date=dealer_review["purchase_date"],
                                   car_make=dealer_review["car_make"], car_model=dealer_review["car_model"],
                                   car_year=dealer_review["car_year"], sentiment = sentiment)
            results.append(reviews_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3b165c56-7142-4732-8deb-d6b0228a06c5"
    api_key = "t8lEGm7AXIYMDJ8fn2chBq7BhSiuNNZSK0QuePL3bco2"
    # params = dict()
    # params["text"] = dealerreview,
    # params["version"] = "2022-04-07"
    # params["features"] = ["sentiment"]
    # params["return_analyzed_text"] = False
    #response = get_request(url, api_key, params=params)

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    try:
        response = natural_language_understanding.analyze(
            text = dealerreview,
            features=Features(sentiment=SentimentOptions())).get_result()
    except:
        return 0
    print(response)
    return response['sentiment']['document']['score']





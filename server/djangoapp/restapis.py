import requests
import json
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
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
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


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
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
    dealer_id = kwargs['id']
    json_result = get_request(url, dealer_id)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # Create a DealerReview object with values in `doc` object
            dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   id=dealer_doc["id"], review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"],
                                   car_make=dealer_doc["car_make"], car_model=dealer_doc["car_model"],
                                   car_year=dealer_doc["car_year"], sentiment=dealer_doc["sentiment"])
            results.append(dealer_obj)

    return results

#parametro de correccion!!!!!
#def get_dealer_reviews_from_cf(url, **kwargs):
#    results = []
#    json_result = get_request(url, id=kwargs['id'])
#    if(json_result):
#        dealer_reviews = json_result
#        for dealer_review in dealer_reviews:
            #sentiment = analyze_review_sentiments(dealer_review['review'])
#            dealer_review_obj = DealerReview(dealership=dealer_review['dealership'], name=dealer_review['name'],
#                                    purchase=dealer_review['purchase'], review=dealer_review['review'], purchase_date=dealer_review['purchase_date'],
#                                   car_make=dealer_review['car_make'], car_model=dealer_review['car_model'], car_year=dealer_review['car_year'],
#                                   id=dealer_review['id'], sentiment=sentiment)
#           results.append(dealer_review_obj)
#   return results

# Get dealer by id
#def get_dealer_by_id(url, **kwargs):
 #   results = []
  #  # Call get_request with a URL parameter
  #  json_result = get_request(url, dealerId=dealerId)
  #  print(json_result)
  #  if json_result:
        # Get the row list in JSON as dealers
  #      dealers = json_result
        # For each dealer object
  #      for dealer in dealers:
            # Get its content in `doc` object
   #         dealer_doc = dealer
    #        if dealer_doc.get("id") == dealerId:
     #           return CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
   #                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
   #                                short_name=dealer_doc["short_name"],
   #                                st=dealer_doc["st"], zip=dealer_doc["zip"])
            # Create a CarDealer object with values in `doc` object
            
    #return None

    #result = get_dealer_by_id_from_cf(url, dealerId)
    #if result:
    # Do something with the dealer information
    #    print(result.full_name, result.address, result.city, ...)
    #else:
    #   print("Dealer not found.")

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative




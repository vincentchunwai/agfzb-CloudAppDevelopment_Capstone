import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.api_exception import ApiException


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    except:
        print("Network exception occurred")


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    print(json_result)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    if json_result:
        reviews = json_result
        for review in reviews:
            if review["purchase"]:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date=review["purchase_date"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"],
                    sentiment=analyze_review_sentiments(review["review"]),
                    id=review['id']
                )
            else:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date=None,
                    car_make=None,
                    car_model=None,
                    car_year=None,
                    sentiment=analyze_review_sentiments(review["review"]),
                    id=review['id']
                )
            results.append(review_obj)
    return results


def get_dealer_by_id_from_cf(url, id):
    results = []

    json_result = get_request(url, id=id)

    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            if "address" in dealer_doc:
                dealer_obj = CarDealer(
                    address=dealer_doc["address"],
                    city=dealer_doc.get("city", ""),
                    full_name=dealer_doc.get("full_name", ""),
                    id=dealer_doc.get("id", ""),
                    lat=dealer_doc.get("lat", ""),
                    long=dealer_doc.get("long", ""),
                    short_name=dealer_doc.get("short_name", ""),
                    st=dealer_doc.get("st", ""),
                    zip=dealer_doc.get("zip", "")
                )
                results.append(dealer_obj)
            else:
                print(f"Error: 'address' key not found in dealer data for ID {id}")

    return results[0] if results else None


def analyze_review_sentiments(dealer_review):
    API_KEY = "k7Ts-MEtvCQz8uxR_5vh6HqBxjnyerrmPdPWwIqO_Lvz"
    NLU_URL = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/30e685a7-3b00-4957-8ffa-b183e0bbacd9'

    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)

    natural_language_understanding.set_service_url(NLU_URL)

    try:
        response = natural_language_understanding.analyze(
            text=dealer_review,
            features=Features(sentiment=SentimentOptions())).get_result()

        label = response['sentiment']['document']['label']
        return label
    except ApiException as e:
        print(f"Error analyzing sentiment: {e}")
        return None



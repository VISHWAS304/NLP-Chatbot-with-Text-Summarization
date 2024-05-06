# feedback_handler.py
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from db_helper import extract_food_item_and_price

def handle_food_feedback(parameters: dict, query_text: str, session_id: str):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(query_text)
    print(sentiment_scores)

    normalized_score = (sentiment_scores['compound'] + 1) * 2.5
    print(normalized_score)

    if normalized_score < 2.5:
        # Negative feedback
        fulfillment_text = f"We're sorry to hear that review {query_text} from you. Your feedback is important to us. Please contact us so we can address this issue promptly."
    elif 2.5 < normalized_score == 2.5:
        # Neutral feedback
        fulfillment_text = f"Thank you for your feedback on the {query_text}. We're glad you found it to be satisfactory. If you have any suggestions for improvement, we'd love to hear them."
    elif normalized_score > 3.5:
        # Positive feedback
        fulfillment_text = f"Thank you for your wonderful feedback! We're thrilled you enjoyed the {query_text}. Your satisfaction means the world to us."
    
    return fulfillment_text

def handle_food_price_feedback(parameters: dict,query_text,session_id: str):
    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(query_text)
    print(sentiment_scores)

    normalized_score = (sentiment_scores['compound'] + 1) * 2.5
    print(normalized_score)

    # Extracting food item name and price
    matched_food_item, matched_price = extract_food_item_and_price(query_text)

    if matched_food_item:
        if normalized_score <= 2.5:
            # Negative feedback
            fulfillment_text = f"We're sorry to hear that review regarding {matched_food_item} priced at ${matched_price} from you. Your feedback is important to us. Please contact us so we can address this issue promptly."
        elif  normalized_score == 2.5:
            # Neutral feedback
            fulfillment_text = f"Thank you for your feedback on the {matched_food_item} priced at ${matched_price}. We're glad you found it to be satisfactory. If you have any suggestions for improvement, we'd love to hear them."
        else:
            # Positive feedback
            fulfillment_text = f"Thank you for your wonderful feedback! We're thrilled you enjoyed the {matched_food_item} priced at ${matched_price}. Your satisfaction means the world to us."        

    else:
        # No matching food item found in the query text
        fulfillment_text = "Thank you for your feedback. We'll take your comments into consideration to improve our services."
    
    return fulfillment_text

def handle_delivery_feedback(parameters: dict, query_text: str, session_id: str):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(query_text)
    print(sentiment_scores)

    normalized_score = (sentiment_scores['compound'] + 1) * 2.5
    print(normalized_score)

    if normalized_score < 3:
        # Negative feedback
        fulfillment_text = "We apologize for any inconvenience caused by the delivery. Your feedback is valuable to us. Please contact us so we can address this issue promptly."
    elif 2.5 <= normalized_score <= 3.5:
        # Neutral feedback
        fulfillment_text = "Thank you for your feedback regarding the delivery. We're glad to hear it was satisfactory. If you have any suggestions for improvement, we're here to listen."
    else:
        # Positive feedback
        fulfillment_text = "We're delighted to hear that you had a positive experience with the delivery! Your satisfaction is our top priority. Thank you for your feedback!"

    return fulfillment_text

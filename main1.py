from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pymongo
from pymongo import MongoClient
import re
import db_helper
from feedback_handler import handle_food_feedback, handle_food_price_feedback, handle_delivery_feedback

app = FastAPI()

inprogress_orders = {}
session_id_mapping = {}
next_numeric_id = 1

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['chat_messages']

def get_numeric_session_id(session_path):
    global next_numeric_id
    alphanumeric_id = session_path.split('/')[-1]
    if alphanumeric_id not in session_id_mapping:
        session_id_mapping[alphanumeric_id] = str(next_numeric_id)
        next_numeric_id += 1
    return session_id_mapping[alphanumeric_id]

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    query_text = payload['queryResult']['queryText']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = get_numeric_session_id(output_contexts[0]["name"])

    print(f"Received intent: {intent}")  # Print the received intent

    # Map intents to their corresponding handler functions
    intent_handler_dict = {
        'order.add - context:ongoing-order': add_to_order,
        'order.remove - context:ongoing-order': remove_from_order,
        'order.complete - context:ongoing-order': complete_order,
        'track.order - context:ongoing-tracking': track_order,
        'track.order': track_order,
        'food.feedback': handle_food_feedback,
        'food_price.feedback': handle_food_price_feedback,
        'delivery.feedback': handle_delivery_feedback
    }

    # Handle the intent
    if intent in intent_handler_dict:
        fulfillment_text = intent_handler_dict[intent](parameters, query_text, session_id)
    else:
        fulfillment_text = "Sorry, I didn't understand that."

    # Save the chat message
    save_chat_message(session_id, query_text, fulfillment_text)

    # Respond to the client
    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def save_chat_message(session_id, query_text, fulfillment_text):
    # Use a session-specific collection
    collection = db[f'session_{session_id}']
    chat_message = {
        'queryText': query_text,
        'fulfillmentText': fulfillment_text
    }
    # Insert the chat message into the database
    collection.insert_one(chat_message)

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    # Insert individual items along with quantity in orders table
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1

    # Now insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                           f"Here is your order id # {order_id}. " \
                           f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return fulfillment_text

def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        print("***************************************************")
        print(inprogress_orders)

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return fulfillment_text

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        return fulfillment_text
    
    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return fulfillment_text

def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return fulfillment_text
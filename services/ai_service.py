import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def interpret_question(question):
    # Use OpenAI to classify the intent
    prompt = f"Analyze this question about Shopify analytics and classify the intent into one of: GET_TOTAL_SALES, GET_AVG_ORDER, GET_TOP_CUSTOMER, GET_INVENTORY_LOW_STOCK, UNKNOWN. Question: '{question}'"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0.5
        )
        intent = response.choices[0].text.strip().upper()
        return intent
    except Exception as e:
        print(f"Error with OpenAI: {e}")
        # Fallback to simple keywords
        question_lower = question.lower()
        if "total sales" in question_lower:
            return "GET_TOTAL_SALES"
        elif "average" in question_lower:
            return "GET_AVG_ORDER"
        elif "top customer" in question_lower:
            return "GET_TOP_CUSTOMER"
        elif "inventory" in question_lower or "stock" in question_lower:
            return "GET_INVENTORY_LOW_STOCK"
        else:
            return "UNKNOWN"

def explain_result(intent, data):
    # Simple explanation based on intent
    if intent == "GET_TOTAL_SALES":
        return f"Based on your orders, the total sales amount to ₹{data['total_sales']:.2f}."
    elif intent == "GET_AVG_ORDER":
        return f"The average order value is ₹{data['average_order_value']:.2f}."
    elif intent == "GET_TOP_CUSTOMER":
        return f"Your top customer by spending is {data['top_customer']}."
    elif intent == "GET_INVENTORY_LOW_STOCK":
        return f"Products low on stock: {', '.join(data['low_stock_products'])}."
    else:
        return "I'm not sure how to answer that."

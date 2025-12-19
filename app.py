from flask import Flask, request, jsonify
from services.shopify_service import get_sales_summary, get_customer_summary, get_inventory_summary
from services.ai_service import interpret_question, explain_result

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    if not data or "question" not in data:
        return jsonify({"error": "Please provide a 'question' in the request body."}), 400

    question = data["question"]
    store_id = data.get("store_id", "default_store")  # Optional store context

    # Interpret the question
    intent = interpret_question(question)

    # Fetch data based on intent
    if intent == "GET_TOTAL_SALES":
        sales_data = get_sales_summary()
        answer = explain_result(intent, sales_data)
        confidence = "high"
    elif intent == "GET_AVG_ORDER":
        sales_data = get_sales_summary()
        answer = explain_result(intent, sales_data)
        confidence = "high"
    elif intent == "GET_TOP_CUSTOMER":
        customer_data = get_customer_summary()
        answer = explain_result(intent, customer_data)
        confidence = "medium"
    elif intent == "GET_INVENTORY_LOW_STOCK":
        inventory_data = get_inventory_summary()
        answer = explain_result(intent, inventory_data)
        confidence = "medium"
    else:
        answer = "Sorry, I couldn't understand your question. Try asking about sales, customers, or inventory."
        confidence = "low"

    return jsonify({
        "store_id": store_id,
        "answer": answer,
        "confidence": confidence
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

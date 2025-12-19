import pandas as pd

def get_sales_summary():
    # Load orders data
    orders = pd.read_csv("data/orders.csv")
    total_sales = orders["total_price"].sum()
    avg_sales = orders["total_price"].mean()
    return {
        "total_sales": total_sales,
        "average_order_value": avg_sales
    }

def get_customer_summary():
    # Load customers data
    customers = pd.read_csv("data/customers.csv")
    total_customers = len(customers)
    top_customer = customers.loc[customers["total_spent"].idxmax()]["name"]
    return {
        "total_customers": total_customers,
        "top_customer": top_customer
    }

def get_inventory_summary():
    # Load inventory and products data
    inventory = pd.read_csv("data/inventory.csv")
    products = pd.read_csv("data/products.csv")
    merged = pd.merge(inventory, products, on="product_id")
    low_stock = merged[merged["available"] < 10]  # Threshold for low stock
    low_stock_products = low_stock["name"].tolist()
    return {
        "low_stock_products": low_stock_products if low_stock_products else ["None"]
    }

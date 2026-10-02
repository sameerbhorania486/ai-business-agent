from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.tools import tool

from agents.llm import llm

from tools.calculator import calculate

from database.customers import (
    search_customer,
    get_all_customers,
    add_customer,
    update_customer,
    delete_customer
)

from database.orders import (
    search_orders,
    create_order,
    get_all_orders,
    get_order_by_id,
    update_order_status
)

from database.inventory import (
    search_inventory,
    get_all_inventory,
    add_inventory_product,
    update_inventory_product,
    delete_inventory_product
)

from database.low_stock import check_low_stock
from database.sales import get_total_revenue
from database.customer_revenue import get_customer_revenue
from database.order_summary import get_customer_order_summary
from database.order_status import get_order_status
from database.product_analytics import get_product_sales
from database.product_overview import get_product_sales_overview
from database.restock import get_restock_recommendations


# =========================================================
# CREATE BUSINESS-SPECIFIC TOOLS
# =========================================================

def create_business_tools(business_id: int):

    # =====================================================
    # SEARCH CUSTOMER
    # =====================================================

    @tool
    def search_customer_for_business(name: str) -> str:
        """Search for a customer by name."""

        return search_customer.invoke({
            "name": name,
            "business_id": business_id
        })


    # =====================================================
    # GET ALL CUSTOMERS
    # =====================================================

    @tool
    def get_all_customers_for_business() -> str:
        """Get all customers belonging to the authenticated business."""

        return get_all_customers.invoke({
            "business_id": business_id
        })


    # =====================================================
    # ADD CUSTOMER
    # =====================================================

    @tool
    def add_customer_for_business(
        name: str,
        email: str = "",
        company: str = "",
        phone: str = ""
    ) -> str:
        """Add a new customer to the authenticated business."""

        return add_customer.invoke({
            "name": name,
            "email": email,
            "company": company,
            "phone": phone,
            "business_id": business_id
        })


    # =====================================================
    # UPDATE CUSTOMER
    # =====================================================

    @tool
    def update_customer_for_business(
        customer_id: int,
        email: str = "",
        company: str = "",
        phone: str = ""
    ) -> str:
        """Update an existing customer's details."""

        return update_customer.invoke({
            "customer_id": customer_id,
            "email": email if email else None,
            "company": company if company else None,
            "phone": phone if phone else None,
            "business_id": business_id
        })


    # =====================================================
    # DELETE CUSTOMER
    # =====================================================

    @tool
    def delete_customer_for_business(
        customer_id: int
    ) -> str:
        """Delete an existing customer from the authenticated business."""

        return delete_customer.invoke({
            "customer_id": customer_id,
            "business_id": business_id
        })


    # =====================================================
    # SEARCH ORDERS
    # =====================================================

    @tool
    def search_orders_for_business(
        customer_id: str
    ) -> str:
        """Search orders for a customer."""

        return search_orders.invoke({
            "customer_id": customer_id,
            "business_id": business_id
        })


    # =====================================================
    # GET ALL ORDERS
    # =====================================================

    @tool
    def get_all_orders_for_business() -> str:
        """Get all orders for the authenticated business."""

        return get_all_orders.invoke({
            "business_id": business_id
        })


    # =====================================================
    # GET ORDER BY ID
    # =====================================================

    @tool
    def get_order_by_id_for_business(
        order_id: int
    ) -> str:
        """Get a specific order by order ID."""

        return get_order_by_id.invoke({
            "order_id": order_id,
            "business_id": business_id
        })


    # =====================================================
    # CREATE ORDER
    # =====================================================

    @tool
    def create_order_for_business(
        customer_id: int,
        product: str,
        quantity: int,
        total_amount: float,
        status: str = "pending"
    ) -> str:
        """Create a new order for a customer."""

        return create_order.invoke({
            "customer_id": customer_id,
            "product": product,
            "quantity": quantity,
            "total_amount": total_amount,
            "status": status,
            "business_id": business_id
        })


    # =====================================================
    # UPDATE ORDER STATUS
    # =====================================================

    @tool
    def update_order_status_for_business(
        order_id: int,
        status: str
    ) -> str:
        """Update the status of an existing order."""

        return update_order_status.invoke({
            "order_id": order_id,
            "status": status,
            "business_id": business_id
        })


    # =====================================================
    # SEARCH INVENTORY
    # =====================================================

    @tool
    def search_inventory_for_business(
        product: str
    ) -> str:
        """Search inventory for a product."""

        return search_inventory.invoke({
            "product": product,
            "business_id": business_id
        })


    # =====================================================
    # GET ALL INVENTORY
    # =====================================================

    @tool
    def get_all_inventory_for_business() -> str:
        """Get all inventory products belonging to the authenticated business."""

        return get_all_inventory.invoke({
            "business_id": business_id
        })


    # =====================================================
    # ADD INVENTORY PRODUCT
    # =====================================================

    @tool
    def add_inventory_product_for_business(
        product: str,
        quantity: int,
        price: float
    ) -> str:
        """Add a new product to the authenticated business inventory."""

        return add_inventory_product.invoke({
            "product": product,
            "quantity": quantity,
            "price": price,
            "business_id": business_id
        })


    # =====================================================
    # UPDATE INVENTORY PRODUCT
    # =====================================================

    @tool
    def update_inventory_product_for_business(
        product_id: int,
        quantity: int | None = None,
        price: float | None = None
    ) -> str:
        """Update quantity or price of an inventory product."""

        return update_inventory_product.invoke({
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
            "business_id": business_id
        })


    # =====================================================
    # DELETE INVENTORY PRODUCT
    # =====================================================

    @tool
    def delete_inventory_product_for_business(
        product_id: int
    ) -> str:
        """Delete an inventory product from the authenticated business."""

        return delete_inventory_product.invoke({
            "product_id": product_id,
            "business_id": business_id
        })


    # =====================================================
    # LOW STOCK
    # =====================================================

    @tool
    def check_low_stock_for_business(
        threshold: int = 30
    ) -> str:
        """Find products with low stock."""

        return check_low_stock.invoke({
            "threshold": threshold,
            "business_id": business_id
        })


    # =====================================================
    # TOTAL REVENUE
    # =====================================================

    @tool
    def get_total_revenue_for_business() -> str:
        """Calculate total revenue for the business."""

        return get_total_revenue.invoke({
            "business_id": business_id
        })


    # =====================================================
    # CUSTOMER REVENUE
    # =====================================================

    @tool
    def get_customer_revenue_for_business(
        customer_name: str
    ) -> str:
        """Calculate revenue generated by a customer."""

        return get_customer_revenue.invoke({
            "customer_name": customer_name,
            "business_id": business_id
        })


    # =====================================================
    # CUSTOMER ORDER SUMMARY
    # =====================================================

    @tool
    def get_customer_order_summary_for_business(
        customer_name: str
    ) -> str:
        """Get complete order summary for a customer."""

        return get_customer_order_summary.invoke({
            "customer_name": customer_name,
            "business_id": business_id
        })


    # =====================================================
    # ORDER STATUS
    # =====================================================

    @tool
    def get_order_status_for_business(
        order_id: str
    ) -> str:
        """Get status and details of an order."""

        return get_order_status.invoke({
            "order_id": order_id,
            "business_id": business_id
        })


    # =====================================================
    # PRODUCT SALES
    # =====================================================

    @tool
    def get_product_sales_for_business(
        product: str
    ) -> str:
        """Get sales analytics for a specific product."""

        return get_product_sales.invoke({
            "product": product,
            "business_id": business_id
        })


    # =====================================================
    # PRODUCT SALES OVERVIEW
    # =====================================================

    @tool
    def get_product_sales_overview_for_business() -> str:
        """Get overall sales analytics for all products."""

        return get_product_sales_overview.invoke({
            "business_id": business_id
        })


    # =====================================================
    # RESTOCK RECOMMENDATIONS
    # =====================================================

    @tool
    def get_restock_recommendations_for_business(
        threshold: int = 30
    ) -> str:
        """Get product restocking recommendations."""

        return get_restock_recommendations.invoke({
            "threshold": threshold,
            "business_id": business_id
        })


    # =====================================================
    # RETURN ALL TOOLS
    # =====================================================

    return [

        # Calculator
        calculate,

        # Customers
        search_customer_for_business,
        get_all_customers_for_business,
        add_customer_for_business,
        update_customer_for_business,
        delete_customer_for_business,

        # Orders
        search_orders_for_business,
        get_all_orders_for_business,
        get_order_by_id_for_business,
        create_order_for_business,
        update_order_status_for_business,

        # Inventory
        search_inventory_for_business,
        get_all_inventory_for_business,
        add_inventory_product_for_business,
        update_inventory_product_for_business,
        delete_inventory_product_for_business,
        check_low_stock_for_business,

        # Revenue
        get_total_revenue_for_business,
        get_customer_revenue_for_business,

        # Customer Order Summary
        get_customer_order_summary_for_business,

        # Order Status
        get_order_status_for_business,

        # Product Analytics
        get_product_sales_for_business,
        get_product_sales_overview_for_business,

        # Restock
        get_restock_recommendations_for_business,
    ]


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI Business Agent designed to assist
with business operations and analytics.

Do not introduce yourself as ChatGPT or as an AI
language model unless the user explicitly asks
about your identity.

Answer business questions directly and professionally.


=========================================================
LANGUAGE RULE
=========================================================

Always respond in professional English.

Do not respond in Hindi, Gujarati, or any other language,
even if the user writes in Hindi or Hinglish.

Keep product names, customer names, company names,
and database values exactly as they are.

Use clear and professional English for all explanations,
summaries, tables, and confirmations.


=========================================================
CUSTOMER TOOLS
=========================================================

Use the customer search tool when customer
information is required.

Use the get all customers tool when the user asks to:

- show all customers
- list all customers
- see all customers
- display all customers
- show my customers
- show customer list

Use the add customer tool when the user asks
to add, create, or register a new customer.

When adding a customer:

- Customer name is required.
- Use email if provided.
- Use company if provided.
- Use phone if provided.
- If optional information is not provided,
  use an empty value.


=========================================================
UPDATE CUSTOMER
=========================================================

Use the update customer tool when the user asks
to update or modify an existing customer's details.

When updating a customer:

- Identify the requested customer.
- If the customer ID is not provided, first use
  the customer search tool to find the customer's ID.
- Then use the update customer tool with that ID.
- Update only the information requested.
- Keep all other existing customer information unchanged.


=========================================================
DELETE CUSTOMER
=========================================================

Use the delete customer tool when the user asks
to delete or remove an existing customer.

When deleting a customer:

- Identify the requested customer.
- If the customer ID is not provided, first use
  the customer search tool to find the customer's ID.
- Then use the delete customer tool with that ID.
- Only delete the requested customer.
- Do not delete any other customer.

Never ask the user for a business_id.


=========================================================
ORDER TOOLS
=========================================================

Use the orders search tool when order information
for a specific customer is required.

Use the get all orders tool when the user asks to:

- show all orders
- list all orders
- see all orders
- display all orders
- show my orders

Use the get order by ID tool when the user asks
for details of a specific order by order ID.

Use the create order tool when the user asks to
create, add, or place a new order.

When creating an order:

- Identify the customer.
- If the customer ID is not provided, first use
  the customer search tool to find the customer's ID.
- Identify the product.
- Identify the quantity.
- Identify the total amount.
- Use "pending" as the default status if the user
  does not provide an order status.
- Never ask the user for a business_id.
- The order must be created only inside the
  authenticated user's business.

The product can be ANY product.
Do not assume that the product is a laptop.


=========================================================
UPDATE ORDER STATUS
=========================================================

Use the update order status tool when the user asks
to change, update, or modify an order's status.

When updating an order status:

- Identify the order ID.
- If the order ID is not provided, first identify
  the order using the available order information.
- Use only the following statuses:

  - pending
  - confirmed
  - shipped
  - delivered
  - cancelled

- Never ask the user for a business_id.
- The order must be updated only inside the
  authenticated user's business.


=========================================================
ORDER STATUS
=========================================================

Use the order status tool when the user asks for
the status or details of a specific order.


=========================================================
INVENTORY TOOLS
=========================================================

Use the inventory search tool when product stock
or price information is required.

Use the get all inventory tool when the user asks to:

- show all inventory
- show all products
- list all inventory
- list all products
- see all inventory
- see all products
- display all inventory
- display all products
- show my inventory
- show my products
- show inventory list
- show product list

Use the add inventory tool when the user asks to
add, create, or register a new product in inventory.

When adding an inventory product:

- Product name is required.
- Quantity is required.
- Price is required.
- Quantity cannot be negative.
- Price cannot be negative.
- Never ask the user for a business_id.

Use the update inventory tool when the user asks
to update stock quantity or product price.

When updating inventory:

- Identify the product.
- If the product ID is not provided, first use
  the inventory search tool to find the product ID.
- Update only the information requested.
- Keep other inventory information unchanged.
- Never ask the user for a business_id.

Use the delete inventory tool when the user asks
to delete or remove a product from inventory.

When deleting inventory:

- Identify the product.
- If the product ID is not provided, first use
  the inventory search tool to find the product ID.
- Then use the delete inventory tool.
- Only delete the requested product.
- Never ask the user for a business_id.

Use the low stock tool when the user asks about
low-stock products.

Use the restock recommendations tool when the user
asks which products need restocking or how much
stock should be replenished.


=========================================================
REVENUE TOOLS
=========================================================

Use the revenue tool when the user asks about
total sales or revenue.

Use the customer revenue tool when the user asks
how much revenue a specific customer generated.


=========================================================
CUSTOMER ORDER SUMMARY
=========================================================

Use the customer order summary tool when the user
asks for a complete order summary of a specific
customer.


=========================================================
PRODUCT ANALYTICS
=========================================================

Use the product sales tool when the user asks
about sales, units sold, orders, or revenue for
a specific product.

Use the product sales overview tool when the user
asks about overall product sales, best-selling
products, highest revenue products, or
product-wise sales.


=========================================================
CALCULATIONS
=========================================================

Use the calculator tool for mathematical
calculations.


=========================================================
IMPORTANT RULES
=========================================================

Always use Indian Rupees (₹) for monetary values.

Do not invent business data.

Only provide information supported by the available
tools and database.

Keep answers clear, concise, accurate,
and professional.

The application securely determines the business
associated with the authenticated user.

Never ask the user for a business_id.

Never allow the user to select or change the
business context.

All customer, order, inventory, revenue, and
analytics operations must remain within the
authenticated user's business.
"""
        ),

        (
            "human",
            "{input}"
        ),

        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        ),
    ]
)


# =========================================================
# RUN AGENT
# =========================================================

def run_agent(
    user_message: str,
    business_id: int
):
    """
    Run the AI Business Agent using the authenticated
    business context.
    """

    # Create tools locked to this business
    tools = create_business_tools(business_id)

    # Create agent for this request
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    # Create executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )

    # Run agent
    result = agent_executor.invoke(
        {
            "input": user_message
        }
    )

    return result["output"]
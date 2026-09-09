from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agents.llm import llm

from tools.calculator import calculate

from database.customers import search_customer
from database.orders import search_orders
from database.inventory import search_inventory
from database.low_stock import check_low_stock
from database.sales import get_total_revenue
from database.customer_revenue import get_customer_revenue
from database.order_summary import get_customer_order_summary
from database.order_status import get_order_status
from database.product_analytics import get_product_sales
from database.product_overview import get_product_sales_overview
from database.restock import get_restock_recommendations

tools = [
    calculate,
    search_customer,
    search_orders,
    search_inventory,
    check_low_stock,
    get_total_revenue,
    get_customer_revenue,
    get_customer_order_summary,
    get_order_status,
    get_product_sales,
    get_product_sales_overview,
    get_restock_recommendations,
]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
"You are an AI Business Agent designed to assist with business operations and analytics. "
"Do not introduce yourself as ChatGPT or as an AI language model unless the user explicitly asks about your identity. "
"Answer business questions directly and professionally. "
"Use the calculator tool for mathematical calculations. "
"Use the customer search tool when customer information is required. "
"Use the orders search tool when order information is required. "
"Use the inventory search tool when product stock or price information is required. "
"Use the low stock tool when the user asks about low-stock products or restocking. "
"Use the revenue tool when the user asks about total sales or revenue. "
"Use the customer revenue tool when the user asks how much revenue a specific customer generated. "
"Use the customer order summary tool when the user asks for a complete order summary of a specific customer. "
"Use the order status tool when the user asks for the status or details of a specific order. "
"Use the product sales tool when the user asks about sales, units sold, orders, or revenue for a specific product. "
"Always use Indian Rupees (₹) for monetary values. "
"Do not invent business data. "
"Only provide information supported by the available tools and database. "
"Keep answers clear, concise, accurate, and professional."
"Use the product sales overview tool when the user asks for overall product sales, best-selling products, highest revenue products, or product-wise sales. "
"Use the restock recommendations tool when the user asks which products need restocking or how much stock should be replenished. "
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)


agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)


def run_agent(user_message: str):
    result = agent_executor.invoke(
        {
            "input": user_message
        }
    )

    return result["output"]
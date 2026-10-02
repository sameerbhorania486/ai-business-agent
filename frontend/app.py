import requests
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Business Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BACKEND CONFIGURATION
# =========================================================

BACKEND_URL = "https://ai-business-agent-sm7c.vercel.app"


# =========================================================
# SESSION STATE
# =========================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================================================
# API HELPERS
# =========================================================

def api_headers():

    token = st.session_state.get("token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def handle_api_error(response, default_message):

    if response.status_code == 401:
        return "Authentication failed. Please log out and log in again."

    try:
        detail = response.json().get(
            "detail",
            default_message
        )

        return str(detail)

    except Exception:
        return default_message


# =========================================================
# AUTH API
# =========================================================

def login_user(email, password):

    try:

        response = requests.post(
            f"{BACKEND_URL}/login",
            json={
                "email": email,
                "password": password
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": handle_api_error(
                response,
                "Login failed."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "error": f"Unable to connect to backend: {e}"
        }


def register_user(
    name,
    email,
    password,
    business_name,
    phone
):

    try:

        response = requests.post(
            f"{BACKEND_URL}/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "business_name": business_name,
                "phone": phone
            },
            timeout=30
        )

        if response.status_code in [200, 201]:
            return response.json()

        return {
            "error": handle_api_error(
                response,
                "Registration failed."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "error": f"Unable to connect to backend: {e}"
        }


# =========================================================
# DASHBOARD API
# =========================================================

def get_dashboard():

    try:

        response = requests.get(
            f"{BACKEND_URL}/dashboard",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        st.error(
            f"Dashboard API Error: {response.status_code}"
        )

        return None

    except requests.exceptions.RequestException as e:

        st.error(
            f"Unable to connect to backend: {e}"
        )

        return None


def get_orders():

    try:

        response = requests.get(
            f"{BACKEND_URL}/dashboard/orders",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return response.json().get(
                "orders",
                []
            )

        st.error(
            f"Orders API Error: {response.status_code}"
        )

        return []

    except requests.exceptions.RequestException as e:

        st.error(
            f"Unable to load orders: {e}"
        )

        return []


def get_inventory():

    try:

        response = requests.get(
            f"{BACKEND_URL}/dashboard/inventory",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return response.json().get(
                "inventory",
                []
            )

        st.error(
            f"Inventory API Error: {response.status_code}"
        )

        return []

    except requests.exceptions.RequestException as e:

        st.error(
            f"Unable to load inventory: {e}"
        )

        return []


def get_dashboard_customers():

    try:

        response = requests.get(
            f"{BACKEND_URL}/dashboard/customers",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return response.json().get(
                "customers",
                []
            )

        st.error(
            f"Customers API Error: {response.status_code}"
        )

        return []

    except requests.exceptions.RequestException as e:

        st.error(
            f"Unable to load customers: {e}"
        )

        return []


# =========================================================
# INVENTORY API
# =========================================================

def inventory_get_all():

    try:

        response = requests.get(
            f"{BACKEND_URL}/inventory/",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Unable to load inventory."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def inventory_search(product):

    try:

        response = requests.get(
            f"{BACKEND_URL}/inventory/search",
            params={
                "product": product
            },
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Inventory search failed."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def inventory_create(
    product,
    quantity,
    price
):

    try:

        response = requests.post(
            f"{BACKEND_URL}/inventory/",
            headers=api_headers(),
            json={
                "product": product,
                "quantity": quantity,
                "price": price
            },
            timeout=30
        )

        if response.status_code in [200, 201]:

            try:
                data = response.json()
            except Exception:
                data = {}

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Inventory product added successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to add inventory product."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def inventory_update(
    product_id,
    quantity,
    price
):

    try:

        response = requests.put(
            f"{BACKEND_URL}/inventory/{product_id}",
            headers=api_headers(),
            json={
                "quantity": quantity,
                "price": price
            },
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Inventory updated successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to update inventory."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def inventory_delete(product_id):

    try:

        response = requests.delete(
            f"{BACKEND_URL}/inventory/{product_id}",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Inventory product deleted successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to delete inventory product."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def inventory_low_stock():

    try:

        response = requests.get(
            f"{BACKEND_URL}/inventory/low-stock",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Unable to load low-stock inventory."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


# =========================================================
# CUSTOMERS API
# =========================================================

def get_customers():

    try:

        response = requests.get(
            f"{BACKEND_URL}/customers/",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Unable to load customers."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def search_customers(name):

    try:

        response = requests.get(
            f"{BACKEND_URL}/customers/search",
            params={
                "name": name
            },
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Search failed."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def add_customer(
    name,
    email,
    company,
    phone
):

    try:

        response = requests.post(
            f"{BACKEND_URL}/customers/",
            headers=api_headers(),
            json={
                "name": name,
                "email": email,
                "company": company,
                "phone": phone
            },
            timeout=30
        )

        if response.status_code in [200, 201]:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Customer added successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to add customer."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def update_customer(
    customer_id,
    email,
    company,
    phone
):

    try:

        response = requests.put(
            f"{BACKEND_URL}/customers/{customer_id}",
            headers=api_headers(),
            json={
                "email": email,
                "company": company,
                "phone": phone
            },
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Customer updated successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to update customer."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def delete_customer(customer_id):

    try:

        response = requests.delete(
            f"{BACKEND_URL}/customers/{customer_id}",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Customer deleted successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to delete customer."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


# =========================================================
# ORDERS API
# =========================================================

def get_all_orders():

    try:

        response = requests.get(
            f"{BACKEND_URL}/orders/",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Unable to load orders."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def create_order(
    customer_id,
    product,
    quantity,
    total_amount,
    status
):

    try:

        response = requests.post(
            f"{BACKEND_URL}/orders/",
            headers=api_headers(),
            json={
                "customer_id": int(customer_id),
                "product": product,
                "quantity": int(quantity),
                "total_amount": float(total_amount),
                "status": status
            },
            timeout=30
        )

        if response.status_code in [200, 201]:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Order created successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to create order."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def update_order_status(
    order_id,
    status
):

    try:

        response = requests.put(
            f"{BACKEND_URL}/orders/{order_id}",
            headers=api_headers(),
            json={
                "status": status
            },
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Order status updated successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to update order status."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


def delete_order(order_id):

    try:

        response = requests.delete(
            f"{BACKEND_URL}/orders/{order_id}",
            headers=api_headers(),
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "success": True,
                "message": data.get(
                    "message",
                    "Order deleted successfully."
                )
            }

        return {
            "success": False,
            "error": handle_api_error(
                response,
                "Failed to delete order."
            )
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Unable to connect to backend: {e}"
        }


# =========================================================
# CHAT API
# =========================================================

def send_chat(message):

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat",
            headers=api_headers(),
            json={
                "message": message
            },
            timeout=120
        )

        if response.status_code == 200:

            data = response.json()

            return (
                data.get("response")
                or data.get("answer")
                or data.get("message")
                or str(data)
            )

        return handle_api_error(
            response,
            "AI request failed."
        )

    except requests.exceptions.RequestException as e:

        return (
            f"Unable to connect to AI backend: {e}"
        )


# =========================================================
# LOGIN / REGISTER PAGE
# =========================================================

if not st.session_state.token:

    st.title("🤖 AI Business Agent")

    st.caption(
        "Intelligent business management powered by AI"
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        [
            "Login",
            "Create Account"
        ]
    )

    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader(
            "Welcome back"
        )

        st.write(
            "Sign in to access your business workspace."
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            width="stretch"
        ):

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                with st.spinner(
                    "Signing in..."
                ):

                    result = login_user(
                        email,
                        password
                    )

                if result and result.get(
                    "access_token"
                ):

                    st.session_state.token = (
                        result["access_token"]
                    )

                    st.session_state.user_email = email

                    st.session_state.user_name = (
                        email.split("@")[0].title()
                    )

                    try:

                        verify_response = requests.get(
                            f"{BACKEND_URL}/dashboard",
                            headers={
                                "Authorization":
                                f"Bearer "
                                f"{st.session_state.token}"
                            },
                            timeout=30
                        )

                        if verify_response.status_code == 200:

                            st.success(
                                "Login successful."
                            )

                            st.rerun()

                        else:

                            st.session_state.token = None

                            st.error(
                                "Login succeeded, but "
                                "dashboard authentication failed."
                            )

                            st.code(
                                f"Status: "
                                f"{verify_response.status_code}\n\n"
                                f"Response:\n"
                                f"{verify_response.text}"
                            )

                    except requests.exceptions.RequestException as e:

                        st.session_state.token = None

                        st.error(
                            f"Unable to verify login: {e}"
                        )

                else:

                    st.error(
                        result.get(
                            "error",
                            "Invalid email or password."
                        )
                    )

    # =====================================================
    # REGISTER
    # =====================================================

    with register_tab:

        st.subheader(
            "Create your business account"
        )

        st.write(
            "Create a secure workspace for your business."
        )

        name = st.text_input(
            "Owner Name",
            placeholder="Your full name",
            key="register_name"
        )

        business_name = st.text_input(
            "Business Name",
            placeholder="Your business name",
            key="register_business"
        )

        register_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="register_email"
        )

        phone = st.text_input(
            "Phone",
            placeholder="Optional",
            key="register_phone"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            width="stretch"
        ):

            if not name:

                st.warning(
                    "Please enter owner name."
                )

            elif not business_name:

                st.warning(
                    "Please enter business name."
                )

            elif not register_email:

                st.warning(
                    "Please enter email."
                )

            elif not register_password:

                st.warning(
                    "Please create a password."
                )

            else:

                with st.spinner(
                    "Creating your account..."
                ):

                    result = register_user(
                        name,
                        register_email,
                        register_password,
                        business_name,
                        phone
                    )

                if result and not result.get(
                    "error"
                ):

                    st.success(
                        "Account created successfully."
                    )

                    st.info(
                        "Go to Login and sign in."
                    )

                else:

                    st.error(
                        result.get(
                            "error",
                            "Registration failed."
                        )
                    )

    st.divider()

    st.caption(
        "AI Business Agent"
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title(
        "🤖 AI Business Agent"
    )

    st.caption(
        "Business workspace"
    )

    st.divider()

    if st.button(
        "Dashboard",
        width="stretch"
    ):

        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button(
        "Customers",
        width="stretch"
    ):

        st.session_state.page = "Customers"
        st.rerun()

    if st.button(
        "Orders",
        width="stretch"
    ):

        st.session_state.page = "Orders"
        st.rerun()

    if st.button(
        "Inventory",
        width="stretch"
    ):

        st.session_state.page = "Inventory"
        st.rerun()

    if st.button(
        "Business Chat",
        width="stretch"
    ):

        st.session_state.page = "Business Chat"
        st.rerun()

    if st.button(
        "Settings",
        width="stretch"
    ):

        st.session_state.page = "Settings"
        st.rerun()

    st.divider()

    st.caption(
        "Signed in as"
    )

    st.write(
        f"**{st.session_state.user_name}**"
    )

    st.caption(
        st.session_state.user_email
    )

    if st.button(
        "Log out",
        width="stretch"
    ):

        st.session_state.token = None
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.session_state.chat_history = []

        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    st.title(
        "Dashboard"
    )

    st.caption(
        "Your business at a glance."
    )

    dashboard = get_dashboard()

    if dashboard is None:
        st.stop()

    user_data = dashboard.get(
        "user",
        {}
    )

    if isinstance(
        user_data,
        dict
    ):

        st.session_state.user_name = user_data.get(
            "name",
            st.session_state.user_name
        )

        st.session_state.user_email = user_data.get(
            "email",
            st.session_state.user_email
        )

    elif isinstance(
        user_data,
        str
    ):

        st.session_state.user_name = user_data

    business_name = dashboard.get(
        "business_name",
        "Your Business"
    )

    st.write(
        f"**{business_name}**"
    )

    st.divider()

    total_customers = dashboard.get(
        "total_customers",
        0
    )

    total_orders = dashboard.get(
        "total_orders",
        0
    )

    total_revenue = dashboard.get(
        "total_revenue",
        0
    )

    low_stock = dashboard.get(
        "low_stock_products",
        0
    )

    total_inventory = dashboard.get(
        "total_inventory",
        0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Customers",
            total_customers
        )

    with col2:

        st.metric(
            "Orders",
            total_orders
        )

    with col3:

        st.metric(
            "Revenue",
            f"₹{float(total_revenue):,.2f}"
        )

    with col4:

        st.metric(
            "Low Stock",
            low_stock
        )

    with col5:

        st.metric(
            "Inventory",
            total_inventory
        )

    st.divider()

    inventory_col, orders_col = st.columns(2)

    with inventory_col:

        st.subheader(
            "Inventory"
        )

        inventory = get_inventory()

        if inventory:

            rows = []

            for item in inventory:

                rows.append(
                    {
                        "Product": item.get(
                            "product",
                            ""
                        ),
                        "Quantity": item.get(
                            "quantity",
                            0
                        ),
                        "Price": (
                            f"₹"
                            f"{float(item.get('price', 0)):,.0f}"
                        ),
                        "Status": (
                            "Low stock"
                            if item.get(
                                "low_stock",
                                False
                            )
                            else "Healthy"
                        )
                    }
                )

            st.dataframe(
                rows,
                width="stretch",
                hide_index=True
            )

        else:

            st.info(
                "No inventory available."
            )

    with orders_col:

        st.subheader(
            "Recent Orders"
        )

        orders = get_orders()

        if orders:

            rows = []

            for order in orders[:10]:

                rows.append(
                    {
                        "Order": order.get(
                            "order_id",
                            ""
                        ),
                        "Product": order.get(
                            "product",
                            ""
                        ),
                        "Qty": order.get(
                            "quantity",
                            0
                        ),
                        "Amount": (
                            f"₹"
                            f"{float(order.get('total_amount', 0)):,.0f}"
                        ),
                        "Status": order.get(
                            "status",
                            ""
                        ).title()
                    }
                )

            st.dataframe(
                rows,
                width="stretch",
                hide_index=True
            )

        else:

            st.info(
                "No orders available."
            )

    st.divider()

    st.subheader(
        "Customers"
    )

    customers = get_dashboard_customers()

    if customers:

        rows = []

        for customer in customers:

            rows.append(
                {
                    "ID": customer.get(
                        "id",
                        ""
                    ),
                    "Name": customer.get(
                        "name",
                        ""
                    ),
                    "Email": customer.get(
                        "email",
                        ""
                    ),
                    "Company": customer.get(
                        "company",
                        ""
                    ),
                    "Phone": customer.get(
                        "phone",
                        ""
                    )
                }
            )

        st.dataframe(
            rows,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No customers available."
        )


# =========================================================
# CUSTOMERS PAGE
# =========================================================

elif st.session_state.page == "Customers":

    st.title(
        "Customers"
    )

    st.caption(
        "Manage your business customers."
    )

    st.divider()

    search_col, refresh_col = st.columns(
        [5, 1]
    )

    with search_col:

        search_name = st.text_input(
            "Search customers",
            placeholder="Search by customer name...",
            key="customer_search"
        )

    with refresh_col:

        st.write("")

        if st.button(
            "Refresh",
            width="stretch"
        ):

            st.rerun()

    if search_name.strip():

        customer_result = search_customers(
            search_name.strip()
        )

    else:

        customer_result = get_customers()

    if not customer_result.get(
        "success"
    ):

        st.error(
            customer_result.get(
                "error",
                "Unable to load customers."
            )
        )

        st.stop()

    customers = customer_result.get(
        "data",
        []
    )

    st.metric(
        "Total Customers",
        len(customers)
    )

    st.divider()

    with st.expander(
        "Add New Customer",
        expanded=False
    ):

        st.subheader(
            "Customer Details"
        )

        add_col1, add_col2 = st.columns(2)

        with add_col1:

            new_name = st.text_input(
                "Name",
                placeholder="Customer name",
                key="new_customer_name"
            )

            new_email = st.text_input(
                "Email",
                placeholder="customer@example.com",
                key="new_customer_email"
            )

        with add_col2:

            new_company = st.text_input(
                "Company",
                placeholder="Company name",
                key="new_customer_company"
            )

            new_phone = st.text_input(
                "Phone",
                placeholder="Phone number",
                key="new_customer_phone"
            )

        if st.button(
            "Add Customer",
            type="primary",
            width="stretch"
        ):

            if not new_name.strip():

                st.warning(
                    "Customer name is required."
                )

            else:

                with st.spinner(
                    "Adding customer..."
                ):

                    result = add_customer(
                        new_name,
                        new_email,
                        new_company,
                        new_phone
                    )

                if result.get(
                    "success"
                ):

                    st.success(
                        result.get(
                            "message",
                            "Customer added successfully."
                        )
                    )

                    st.rerun()

                else:

                    st.error(
                        result.get(
                            "error",
                            "Failed to add customer."
                        )
                    )

    st.divider()

    st.subheader(
        "Customer Directory"
    )

    if not customers:

        st.info(
            "No customers found."
        )

    else:

        for customer in customers:

            customer_id = customer.get(
                "id"
            )

            name = customer.get(
                "name",
                ""
            )

            email = customer.get(
                "email",
                ""
            )

            company = customer.get(
                "company",
                ""
            )

            phone = customer.get(
                "phone",
                ""
            )

            with st.expander(
                f"{name}  •  "
                f"{company or 'No company'}"
            ):

                st.write(
                    f"**Customer ID:** {customer_id}"
                )

                edit_col1, edit_col2 = st.columns(2)

                with edit_col1:

                    edit_email = st.text_input(
                        "Email",
                        value=email or "",
                        key=f"edit_email_{customer_id}"
                    )

                    edit_company = st.text_input(
                        "Company",
                        value=company or "",
                        key=f"edit_company_{customer_id}"
                    )

                with edit_col2:

                    edit_phone = st.text_input(
                        "Phone",
                        value=phone or "",
                        key=f"edit_phone_{customer_id}"
                    )

                action_col1, action_col2 = st.columns(2)

                with action_col1:

                    if st.button(
                        "Save Changes",
                        key=f"save_{customer_id}",
                        type="primary",
                        width="stretch"
                    ):

                        with st.spinner(
                            "Updating customer..."
                        ):

                            result = update_customer(
                                customer_id,
                                edit_email,
                                edit_company,
                                edit_phone
                            )

                        if result.get(
                            "success"
                        ):

                            st.success(
                                result.get(
                                    "message",
                                    "Customer updated successfully."
                                )
                            )

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Failed to update customer."
                                )
                            )

                with action_col2:

                    if st.button(
                        "Delete Customer",
                        key=f"delete_{customer_id}",
                        width="stretch"
                    ):

                        with st.spinner(
                            "Deleting customer..."
                        ):

                            result = delete_customer(
                                customer_id
                            )

                        if result.get(
                            "success"
                        ):

                            st.success(
                                result.get(
                                    "message",
                                    "Customer deleted successfully."
                                )
                            )

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Failed to delete customer."
                                )
                            )


# =========================================================
# ORDERS PAGE
# =========================================================

elif st.session_state.page == "Orders":

    st.title(
        "Orders"
    )

    st.caption(
        "Create and manage your business orders."
    )

    st.divider()

    refresh_col1, refresh_col2 = st.columns(
        [5, 1]
    )

    with refresh_col2:

        if st.button(
            "🔄 Refresh",
            width="stretch",
            key="orders_refresh"
        ):

            st.rerun()

    st.divider()

    orders_result = get_all_orders()

    if not orders_result.get(
        "success"
    ):

        st.error(
            orders_result.get(
                "error",
                "Unable to load orders."
            )
        )

        st.stop()

    orders_data = orders_result.get(
        "data",
        {}
    )

    if isinstance(
        orders_data,
        dict
    ):

        orders = orders_data.get(
            "orders",
            []
        )

    elif isinstance(
        orders_data,
        list
    ):

        orders = orders_data

    else:

        orders = []

    total_orders_count = len(orders)

    total_order_revenue = sum(
        float(order.get("total_amount", 0))
        for order in orders
    )

    pending_orders = sum(
        1
        for order in orders
        if str(order.get("status", "")).lower()
        == "pending"
    )

    delivered_orders = sum(
        1
        for order in orders
        if str(order.get("status", "")).lower()
        == "delivered"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Orders",
            total_orders_count
        )

    with col2:

        st.metric(
            "Order Value",
            f"₹{total_order_revenue:,.2f}"
        )

    with col3:

        st.metric(
            "Pending",
            pending_orders
        )

    with col4:

        st.metric(
            "Delivered",
            delivered_orders
        )

    st.divider()

    with st.expander(
        "Create New Order",
        expanded=False
    ):

        st.subheader(
            "Order Details"
        )

        customer_result = get_customers()

        if not customer_result.get(
            "success"
        ):

            st.error(
                customer_result.get(
                    "error",
                    "Unable to load customers."
                )
            )

        else:

            customers_for_order = customer_result.get(
                "data",
                []
            )

            if not customers_for_order:

                st.warning(
                    "Please add a customer before creating an order."
                )

            else:

                customer_options = {}

                for customer in customers_for_order:

                    customer_id = customer.get(
                        "id"
                    )

                    customer_name = customer.get(
                        "name",
                        "Unknown Customer"
                    )

                    company = customer.get(
                        "company",
                        ""
                    )

                    label = (
                        f"{customer_name}"
                        f"{' - ' + company if company else ''}"
                        f" (ID: {customer_id})"
                    )

                    customer_options[label] = customer_id

                selected_customer = st.selectbox(
                    "Customer",
                    list(customer_options.keys()),
                    key="new_order_customer"
                )

                order_col1, order_col2 = st.columns(2)

                with order_col1:

                    order_product = st.text_input(
                        "Product",
                        placeholder="e.g. Samsung Galaxy S25",
                        key="new_order_product"
                    )

                    order_quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        value=1,
                        step=1,
                        key="new_order_quantity"
                    )

                with order_col2:

                    order_amount = st.number_input(
                        "Total Amount",
                        min_value=0.0,
                        value=0.0,
                        step=100.0,
                        key="new_order_amount"
                    )

                    order_status = st.selectbox(
                        "Status",
                        [
                            "pending",
                            "confirmed",
                            "processing",
                            "shipped",
                            "delivered",
                            "cancelled"
                        ],
                        key="new_order_status"
                    )

                if st.button(
                    "Create Order",
                    type="primary",
                    width="stretch",
                    key="create_order_button"
                ):

                    if not order_product.strip():

                        st.warning(
                            "Product name is required."
                        )

                    elif order_amount <= 0:

                        st.warning(
                            "Total amount must be greater than 0."
                        )

                    else:

                        selected_customer_id = customer_options[
                            selected_customer
                        ]

                        with st.spinner(
                            "Creating order..."
                        ):

                            result = create_order(
                                selected_customer_id,
                                order_product.strip(),
                                int(order_quantity),
                                float(order_amount),
                                order_status
                            )

                        if result.get(
                            "success"
                        ):

                            st.success(
                                result.get(
                                    "message",
                                    "Order created successfully."
                                )
                            )

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Failed to create order."
                                )
                            )

    st.divider()

    st.subheader(
        "Order Directory"
    )

    if not orders:

        st.info(
            "No orders found."
        )

    else:

        for order in orders:

            order_id = order.get(
                "order_id",
                ""
            )

            customer_id = order.get(
                "customer_id",
                ""
            )

            product = order.get(
                "product",
                ""
            )

            quantity = order.get(
                "quantity",
                0
            )

            total_amount = float(
                order.get(
                    "total_amount",
                    0
                )
            )

            current_status = str(
                order.get(
                    "status",
                    "pending"
                )
            ).lower()

            status_options = [
                "pending",
                "confirmed",
                "processing",
                "shipped",
                "delivered",
                "cancelled"
            ]

            with st.expander(
                f"Order #{order_id}  •  "
                f"{product}  •  "
                f"₹{total_amount:,.0f}  •  "
                f"{current_status.title()}"
            ):

                st.write(
                    f"**Order ID:** {order_id}"
                )

                st.write(
                    f"**Customer ID:** {customer_id}"
                )

                st.write(
                    f"**Product:** {product}"
                )

                st.write(
                    f"**Quantity:** {quantity}"
                )

                st.write(
                    f"**Total Amount:** "
                    f"₹{total_amount:,.2f}"
                )

                st.divider()

                update_col1, update_col2 = st.columns(2)

                with update_col1:

                    current_index = (
                        status_options.index(current_status)
                        if current_status in status_options
                        else 0
                    )

                    new_status = st.selectbox(
                        "Order Status",
                        status_options,
                        index=current_index,
                        key=f"order_status_{order_id}"
                    )

                with update_col2:

                    st.write("")

                    if st.button(
                        "Update Status",
                        key=f"update_order_{order_id}",
                        type="primary",
                        width="stretch"
                    ):

                        with st.spinner(
                            "Updating order..."
                        ):

                            result = update_order_status(
                                order_id,
                                new_status
                            )

                        if result.get(
                            "success"
                        ):

                            st.success(
                                result.get(
                                    "message",
                                    "Order status updated successfully."
                                )
                            )

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Failed to update order status."
                                )
                            )

                st.divider()

                if st.button(
                    "Delete Order",
                    key=f"delete_order_{order_id}",
                    width="stretch"
                ):

                    with st.spinner(
                        "Deleting order..."
                    ):

                        result = delete_order(
                            order_id
                        )

                    if result.get(
                        "success"
                    ):

                        st.success(
                            result.get(
                                "message",
                                "Order deleted successfully."
                            )
                        )

                        st.rerun()

                    else:

                        st.error(
                            result.get(
                                "error",
                                "Failed to delete order."
                            )
                        )


# =========================================================
# INVENTORY PAGE
# =========================================================

elif st.session_state.page == "Inventory":

    st.title(
        "Inventory Management"
    )

    st.caption(
        "Manage your products, stock quantities and prices."
    )

    st.divider()

    inventory_result = inventory_get_all()

    if not inventory_result.get(
        "success"
    ):

        st.error(
            inventory_result.get(
                "error",
                "Unable to load inventory."
            )
        )

        st.stop()

    inventory_data = inventory_result.get(
        "data",
        {}
    )

    inventory = inventory_data.get(
        "inventory",
        []
    )

    total_products = len(inventory)

    total_units = sum(
        int(item.get("quantity", 0))
        for item in inventory
    )

    low_stock_count = sum(
        1
        for item in inventory
        if int(item.get("quantity", 0)) <= 30
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Products",
            total_products
        )

    with col2:

        st.metric(
            "Total Units",
            total_units
        )

    with col3:

        st.metric(
            "Low Stock Products",
            low_stock_count
        )

    st.divider()

    search_col, refresh_col = st.columns(
        [5, 1]
    )

    with search_col:

        inventory_search_text = st.text_input(
            "Search inventory",
            placeholder="Search by product name...",
            key="inventory_search"
        )

    with refresh_col:

        st.write("")

        if st.button(
            "Refresh",
            width="stretch",
            key="inventory_refresh"
        ):

            st.rerun()

    if inventory_search_text.strip():

        search_result = inventory_search(
            inventory_search_text.strip()
        )

        if search_result.get(
            "success"
        ):

            display_data = search_result.get(
                "data",
                {}
            )

            display_inventory = display_data.get(
                "inventory",
                []
            )

        else:

            st.error(
                search_result.get(
                    "error",
                    "Inventory search failed."
                )
            )

            display_inventory = []

    else:

        display_inventory = inventory

    with st.expander(
        "Add New Product",
        expanded=False
    ):

        st.subheader(
            "Product Details"
        )

        add_inventory_col1, add_inventory_col2 = st.columns(2)

        with add_inventory_col1:

            new_product = st.text_input(
                "Product Name",
                placeholder="e.g. Samsung Galaxy S25",
                key="new_inventory_product"
            )

            new_quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=0,
                step=1,
                key="new_inventory_quantity"
            )

        with add_inventory_col2:

            new_price = st.number_input(
                "Price",
                min_value=0.0,
                value=0.0,
                step=100.0,
                key="new_inventory_price"
            )

            st.write("")

        if st.button(
            "Add Product",
            type="primary",
            width="stretch",
            key="add_inventory_button"
        ):

            if not new_product.strip():

                st.warning(
                    "Product name is required."
                )

            else:

                with st.spinner(
                    "Adding product..."
                ):

                    result = inventory_create(
                        new_product.strip(),
                        int(new_quantity),
                        float(new_price)
                    )

                if result.get(
                    "success"
                ):

                    st.success(
                        result.get(
                            "message",
                            "Inventory product added successfully."
                        )
                    )

                    st.rerun()

                else:

                    st.error(
                        result.get(
                            "error",
                            "Failed to add product."
                        )
                    )

    st.divider()

    with st.expander(
        "Low Stock Products",
        expanded=False
    ):

        low_stock_result = inventory_low_stock()

        if not low_stock_result.get(
            "success"
        ):

            st.error(
                low_stock_result.get(
                    "error",
                    "Unable to load low-stock products."
                )
            )

        else:

            low_stock_data = low_stock_result.get(
                "data",
                {}
            )

            low_stock_inventory = low_stock_data.get(
                "inventory",
                []
            )

            if low_stock_inventory:

                low_stock_rows = []

                for item in low_stock_inventory:

                    low_stock_rows.append(
                        {
                            "Product ID": item.get(
                                "product_id",
                                ""
                            ),
                            "Product": item.get(
                                "product",
                                ""
                            ),
                            "Quantity": item.get(
                                "quantity",
                                0
                            ),
                            "Price": (
                                f"₹"
                                f"{float(item.get('price', 0)):,.0f}"
                            )
                        }
                    )

                st.dataframe(
                    low_stock_rows,
                    width="stretch",
                    hide_index=True
                )

            else:

                st.success(
                    "No low-stock products."
                )

    st.divider()

    st.subheader(
        "Product Directory"
    )

    if not display_inventory:

        st.info(
            "No inventory products found."
        )

    else:

        for item in display_inventory:

            product_id = item.get(
                "product_id"
            )

            product_name = item.get(
                "product",
                ""
            )

            quantity = int(
                item.get(
                    "quantity",
                    0
                )
            )

            price = float(
                item.get(
                    "price",
                    0
                )
            )

            status = (
                "Low stock"
                if quantity <= 30
                else "Healthy"
            )

            with st.expander(
                f"{product_name}  •  "
                f"{quantity} units  •  "
                f"{status}"
            ):

                st.write(
                    f"**Product ID:** {product_id}"
                )

                edit_col1, edit_col2 = st.columns(2)

                with edit_col1:

                    edit_quantity = st.number_input(
                        "Quantity",
                        min_value=0,
                        value=quantity,
                        step=1,
                        key=f"inventory_quantity_{product_id}"
                    )

                with edit_col2:

                    edit_price = st.number_input(
                        "Price",
                        min_value=0.0,
                        value=price,
                        step=100.0,
                        key=f"inventory_price_{product_id}"
                    )

                st.write(
                    f"**Current Status:** {status}"
                )

                action_col1, action_col2 = st.columns(2)

                with action_col1:

                    if st.button(
                        "Save Changes",
                        key=f"inventory_save_{product_id}",
                        type="primary",
                        width="stretch"
                    ):

                        with st.spinner(
                            "Updating product..."
                        ):

                            result = inventory_update(
                                product_id,
                                int(edit_quantity),
                                float(edit_price)
                            )

                        if result.get(
                            "success"
                        ):

                            st.success(
                                result.get(
                                    "message",
                                    "Inventory updated successfully."
                                )
                            )

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Failed to update inventory."
                                )
                            )

                with action_col2:

                    if st.button(
                        "Delete Product",
                        key=f"inventory_delete_{product_id}",
                        width="stretch"
                    ):

                        with st.spinner(
                            "Deleting product..."
                        ):

                            result = inventory_delete(
                                product_id
                            )

                        if result.get(
                            "success"
                        ):

                            st.success(
                                result.get(
                                    "message",
                                    "Inventory product deleted successfully."
                                )
                            )

                            st.rerun()

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Failed to delete product."
                                )
                            )


# =========================================================
# BUSINESS CHAT
# =========================================================

elif st.session_state.page == "Business Chat":

    st.title(
        "Business Chat"
    )

    st.caption(
        "Ask questions about your business data."
    )

    st.divider()

    st.subheader(
        "What can your AI agent do?"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.info(
            "**Customers**\n\n"
            "Search and manage customer information."
        )

    with col2:

        st.info(
            "**Inventory**\n\n"
            "Check products, stock and prices."
        )

    with col3:

        st.info(
            "**Orders**\n\n"
            "Search orders and manage statuses."
        )

    with col4:

        st.info(
            "**Sales**\n\n"
            "Analyze revenue and business performance."
        )

    st.divider()

    st.success(
        "AI Agent is online"
    )

    for chat in st.session_state.chat_history:

        with st.chat_message(
            chat["role"]
        ):

            st.write(
                chat["message"]
            )

    message = st.chat_input(
        "Message your business AI..."
    )

    if message:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "message": message
            }
        )

        with st.chat_message(
            "user"
        ):

            st.write(
                message
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                answer = send_chat(
                    message
                )

            st.write(
                answer
            )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "message": answer
            }
        )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.title(
        "Settings"
    )

    st.caption(
        "Manage your account and application information."
    )

    st.divider()

    st.subheader(
        "Account"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Name",
            value=st.session_state.user_name,
            disabled=True
        )

    with col2:

        st.text_input(
            "Email",
            value=st.session_state.user_email,
            disabled=True
        )

    st.divider()

    st.subheader(
        "AI Capabilities"
    )

    capabilities = [
        "Customer management",
        "Order management",
        "Inventory management",
        "Low-stock detection",
        "Sales analysis",
        "Revenue analysis",
        "Customer revenue analysis",
        "Product analytics",
        "Restock assistance"
    ]

    for capability in capabilities:

        st.write(
            f"✓ {capability}"
        )

    st.divider()

    st.subheader(
        "Security"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            "JWT Authentication enabled"
        )

    with col2:

        st.success(
            "Business data isolation enabled"
        )

    st.divider()

    st.subheader(
        "Technology"
    )

    st.write(
        "**Frontend:** Streamlit"
    )

    st.write(
        "**Backend:** FastAPI"
    )

    st.write(
        "**AI:** LangChain + Groq"
    )

    st.write(
        "**Database:** Supabase / PostgreSQL"
    )

    st.write(
        "**Authentication:** JWT"
    )

    st.divider()

    st.caption(
        "AI Business Agent"
    )

    st.write(
        "• Customer information"
    )

    st.write(
        "• Order information"
    )

    st.write(
        "• Inventory management"
    )

    st.write(
        "• Revenue analytics"
    )

    st.write(
        "• Product sales analytics"
    )

    st.write(
        "• Low-stock detection"
    )

    st.write(
        "• Restock recommendations"
    )

    st.write(
        "• Mathematical calculations"
    )

    st.divider()

    st.info(
        "Your account uses JWT-based authentication."
    )

    st.caption(
        "Intelligent business management powered by AI."
    )
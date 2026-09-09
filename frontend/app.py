import requests
import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Business Agent",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# BACKEND CONFIGURATION
# ==========================================

BACKEND_URL = "http://127.0.0.1:8000"


# ==========================================
# SESSION STATE
# ==========================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# LOGIN FUNCTION
# ==========================================

def login_user(email, password):

    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.token = data["access_token"]

            st.session_state.user = {
                "name": data.get("name", email.split("@")[0]),
                "email": email
            }

            return True, "Login successful."

        try:
            error = response.json().get(
                "detail",
                "Invalid email or password."
            )
        except Exception:
            error = "Invalid email or password."

        return False, error

    except requests.exceptions.ConnectionError:
        return False, "Backend is not running."

    except requests.exceptions.Timeout:
        return False, "Request timed out."

    except Exception as e:
        return False, str(e)


# ==========================================
# REGISTER FUNCTION
# ==========================================

def register_user(name, email, password):

    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={
                "name": name,
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:
            return True, "Registration successful. Please login."

        try:
            error = response.json().get(
                "detail",
                "Registration failed."
            )
        except Exception:
            error = "Registration failed."

        return False, error

    except requests.exceptions.ConnectionError:
        return False, "Backend is not running."

    except requests.exceptions.Timeout:
        return False, "Request timed out."

    except Exception as e:
        return False, str(e)


# ==========================================
# CHAT FUNCTION
# ==========================================

def ask_backend(message):

    if not st.session_state.token:
        return "Please login first."

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": message
            },
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:

            data = response.json()

            return data.get(
                "response",
                "No response received."
            )

        if response.status_code == 401:

            st.session_state.token = None
            st.session_state.user = None

            return "Session expired. Please login again."

        try:
            return response.json().get(
                "detail",
                "Something went wrong."
            )
        except Exception:
            return "Something went wrong."

    except requests.exceptions.ConnectionError:
        return "Backend is not running."

    except requests.exceptions.Timeout:
        return "Request timed out."

    except Exception as e:
        return str(e)


# ==========================================
# DASHBOARD FUNCTION
# ==========================================

def get_dashboard():

    if not st.session_state.token:
        return None

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    try:

        response = requests.get(
            f"{BACKEND_URL}/dashboard",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:

            st.session_state.token = None
            st.session_state.user = None

            return None

        return None

    except Exception:
        return None


# ==========================================
# LOGIN / REGISTER SCREEN
# ==========================================

if not st.session_state.token:

    st.title("🤖 AI Business Agent")

    st.write(
        "AI-powered business operations and analytics platform."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # ======================================
    # LOGIN
    # ======================================

    with login_tab:

        st.header("Welcome Back")

        login_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if not login_email or not login_password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                success, message = login_user(
                    login_email,
                    login_password
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

    # ======================================
    # REGISTER
    # ======================================

    with register_tab:

        st.header("Create Account")

        register_name = st.text_input(
            "Name",
            placeholder="Enter your name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="register_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if (
                not register_name
                or not register_email
                or not register_password
            ):

                st.warning(
                    "Please fill all fields."
                )

            else:

                success, message = register_user(
                    register_name,
                    register_email,
                    register_password
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)

    st.stop()


# ==========================================
# LOGGED-IN USER INFORMATION
# ==========================================

user_name = st.session_state.user.get(
    "name",
    "User"
)

user_email = st.session_state.user.get(
    "email",
    ""
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 AI Business Agent")

    st.divider()

    st.write(f"**User:** {user_name}")

    st.caption(user_email)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "💬 Business Chat",
            "⚙️ Settings"
        ]
    )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.token = None
        st.session_state.user = None
        st.session_state.messages = []

        st.rerun()


# ==========================================
# DASHBOARD
# ==========================================

if page == "📊 Dashboard":

    st.title("📊 Business Dashboard")

    st.write(
        "Overview of your business performance."
    )

    st.divider()

    dashboard = get_dashboard()

    if dashboard:

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Customers",
                dashboard.get(
                    "total_customers",
                    0
                )
            )

        with col2:

            st.metric(
                "Total Orders",
                dashboard.get(
                    "total_orders",
                    0
                )
            )

        with col3:

            revenue = dashboard.get(
                "total_revenue",
                0
            )

            st.metric(
                "Total Revenue",
                f"₹{revenue:,.2f}"
            )

        with col4:

            st.metric(
                "Low Stock Products",
                dashboard.get(
                    "low_stock_products",
                    0
                )
            )

        st.divider()

        st.subheader("📦 Inventory")

        st.metric(
            "Total Inventory",
            dashboard.get(
                "total_inventory",
                0
            )
        )

    else:

        st.error(
            "Unable to load dashboard data."
        )


# ==========================================
# BUSINESS CHAT
# ==========================================

elif page == "💬 Business Chat":

    st.title("💬 Business Chat")

    st.write(
        "Ask questions about customers, orders, "
        "inventory, sales and revenue."
    )

    st.divider()

    # Show previous messages

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # Chat input

    user_message = st.chat_input(
        "Ask your business question..."
    )

    if user_message:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        with st.chat_message("user"):

            st.write(
                user_message
            )

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing business data..."
            ):

                response = ask_backend(
                    user_message
                )

            st.write(
                response
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


# ==========================================
# SETTINGS
# ==========================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.write(
        "Manage your AI Business Agent account."
    )

    st.divider()

    st.subheader("Account")

    st.write(
        f"**Name:** {user_name}"
    )

    st.write(
        f"**Email:** {user_email}"
    )

    st.divider()

    st.subheader("AI Business Agent")

    st.write(
        "Available capabilities:"
    )

    st.write("• Customer information")
    st.write("• Order information")
    st.write("• Inventory management")
    st.write("• Revenue analytics")
    st.write("• Product sales analytics")
    st.write("• Low-stock detection")
    st.write("• Restock recommendations")
    st.write("• Mathematical calculations")

    st.divider()

    st.info(
        "Your account uses JWT-based authentication."
    )
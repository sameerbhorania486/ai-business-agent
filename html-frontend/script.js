// =========================================================
// BACKEND CONFIGURATION
// =========================================================

const BACKEND_URL =
    "https://ai-business-agent-iga7qjvqc-sameerbhorania486.vercel.app";


// =========================================================
// TAB SWITCHING
// =========================================================

function showLogin() {

    const loginSection =
        document.getElementById("loginSection");

    const registerSection =
        document.getElementById("registerSection");

    const loginTab =
        document.getElementById("loginTab");

    const registerTab =
        document.getElementById("registerTab");


    if (loginSection) {

        loginSection.classList.remove("hidden");

    }

    if (registerSection) {

        registerSection.classList.add("hidden");

    }

    if (loginTab) {

        loginTab.classList.add("active");

    }

    if (registerTab) {

        registerTab.classList.remove("active");

    }
}


function showRegister() {

    const loginSection =
        document.getElementById("loginSection");

    const registerSection =
        document.getElementById("registerSection");

    const loginTab =
        document.getElementById("loginTab");

    const registerTab =
        document.getElementById("registerTab");


    if (registerSection) {

        registerSection.classList.remove("hidden");

    }

    if (loginSection) {

        loginSection.classList.add("hidden");

    }

    if (registerTab) {

        registerTab.classList.add("active");

    }

    if (loginTab) {

        loginTab.classList.remove("active");

    }
}


// =========================================================
// API ERROR HANDLER
// =========================================================

async function getApiError(response, defaultMessage) {

    try {

        const data = await response.json();

        return (
            data.detail ||
            data.message ||
            defaultMessage
        );

    } catch (error) {

        return (
            response.statusText ||
            defaultMessage
        );

    }
}


// =========================================================
// LOGIN
// =========================================================

async function loginUser(event) {

    // IMPORTANT:
    // Prevent normal HTML form submission.
    // Without this, browser can reload index.html.

    if (event) {

        event.preventDefault();

    }


    const emailInput =
        document.getElementById("loginEmail");

    const passwordInput =
        document.getElementById("loginPassword");

    const messageElement =
        document.getElementById("loginMessage");


    if (!emailInput || !passwordInput) {

        console.error(
            "Login input elements not found."
        );

        return;

    }


    const email =
        emailInput.value.trim().toLowerCase();

    const password =
        passwordInput.value;


    // -----------------------------------------------------
    // VALIDATION
    // -----------------------------------------------------

    if (!email) {

        showMessage(
            messageElement,
            "Please enter your email.",
            "error"
        );

        return;

    }


    if (!password) {

        showMessage(
            messageElement,
            "Please enter your password.",
            "error"
        );

        return;

    }


    // -----------------------------------------------------
    // LOADING MESSAGE
    // -----------------------------------------------------

    showMessage(
        messageElement,
        "Signing in...",
        "loading"
    );


    try {

        // -------------------------------------------------
        // LOGIN API REQUEST
        // -------------------------------------------------

        const response = await fetch(
            `${BACKEND_URL}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );


        // -------------------------------------------------
        // HANDLE LOGIN ERROR
        // -------------------------------------------------

        if (!response.ok) {

            const errorMessage =
                await getApiError(
                    response,
                    "Invalid email or password."
                );

            showMessage(
                messageElement,
                errorMessage,
                "error"
            );

            return;

        }


        // -------------------------------------------------
        // LOGIN RESPONSE
        // -------------------------------------------------

        const data =
            await response.json();


        console.log(
            "LOGIN RESPONSE:",
            data
        );


        // -------------------------------------------------
        // CHECK TOKEN
        // -------------------------------------------------

        if (!data.access_token) {

            showMessage(
                messageElement,
                "Login succeeded, but no access token was received.",
                "error"
            );

            console.error(
                "No access_token in login response:",
                data
            );

            return;

        }


        // -------------------------------------------------
        // SAVE JWT TOKEN
        // -------------------------------------------------

        localStorage.setItem(
            "access_token",
            data.access_token
        );


        // -------------------------------------------------
        // SAVE USER EMAIL
        // -------------------------------------------------

        localStorage.setItem(
            "user_email",
            email
        );


        // -------------------------------------------------
        // SUCCESS
        // -------------------------------------------------

        showMessage(
            messageElement,
            "Login successful. Opening dashboard...",
            "success"
        );


        // -------------------------------------------------
        // REDIRECT TO DASHBOARD
        // -------------------------------------------------

        setTimeout(() => {

            window.location.href =
                "dashboard.html";

        }, 700);


    } catch (error) {

        console.error(
            "LOGIN ERROR:",
            error
        );


        showMessage(
            messageElement,
            "Unable to connect to the backend. Please try again.",
            "error"
        );

    }

}


// =========================================================
// REGISTER
// =========================================================

async function registerUser(event) {

    // IMPORTANT:
    // Prevent normal HTML form submission.

    if (event) {

        event.preventDefault();

    }


    const nameInput =
        document.getElementById("registerName");

    const businessInput =
        document.getElementById("registerBusiness");

    const emailInput =
        document.getElementById("registerEmail");

    const phoneInput =
        document.getElementById("registerPhone");

    const passwordInput =
        document.getElementById("registerPassword");

    const messageElement =
        document.getElementById("registerMessage");


    if (
        !nameInput ||
        !businessInput ||
        !emailInput ||
        !passwordInput
    ) {

        console.error(
            "Registration input elements not found."
        );

        return;

    }


    const name =
        nameInput.value.trim();

    const businessName =
        businessInput.value.trim();

    const email =
        emailInput.value.trim().toLowerCase();

    const phone =
        phoneInput
            ? phoneInput.value.trim()
            : "";

    const password =
        passwordInput.value;


    // -----------------------------------------------------
    // VALIDATION
    // -----------------------------------------------------

    if (!name) {

        showMessage(
            messageElement,
            "Please enter your name.",
            "error"
        );

        return;

    }


    if (!businessName) {

        showMessage(
            messageElement,
            "Please enter your business name.",
            "error"
        );

        return;

    }


    if (!email) {

        showMessage(
            messageElement,
            "Please enter your email.",
            "error"
        );

        return;

    }


    if (!password) {

        showMessage(
            messageElement,
            "Please create a password.",
            "error"
        );

        return;

    }


    if (password.length < 6) {

        showMessage(
            messageElement,
            "Password should be at least 6 characters.",
            "error"
        );

        return;

    }


    // -----------------------------------------------------
    // LOADING
    // -----------------------------------------------------

    showMessage(
        messageElement,
        "Creating your account...",
        "loading"
    );


    try {

        // -------------------------------------------------
        // REGISTER API REQUEST
        // -------------------------------------------------

        const response = await fetch(
            `${BACKEND_URL}/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    business_name: businessName,
                    phone: phone
                })
            }
        );


        // -------------------------------------------------
        // HANDLE REGISTRATION ERROR
        // -------------------------------------------------

        if (!response.ok) {

            const errorMessage =
                await getApiError(
                    response,
                    "Registration failed."
                );

            showMessage(
                messageElement,
                errorMessage,
                "error"
            );

            return;

        }


        // -------------------------------------------------
        // REGISTER RESPONSE
        // -------------------------------------------------

        const data =
            await response.json();


        console.log(
            "REGISTER RESPONSE:",
            data
        );


        // -------------------------------------------------
        // SUCCESS
        // -------------------------------------------------

        showMessage(
            messageElement,
            "Account created successfully. Please login.",
            "success"
        );


        // -------------------------------------------------
        // CLEAR FORM
        // -------------------------------------------------

        nameInput.value = "";

        businessInput.value = "";

        emailInput.value = "";

        if (phoneInput) {

            phoneInput.value = "";

        }

        passwordInput.value = "";


        // -------------------------------------------------
        // GO TO LOGIN
        // -------------------------------------------------

        setTimeout(() => {

            showLogin();

        }, 1200);


    } catch (error) {

        console.error(
            "REGISTER ERROR:",
            error
        );


        showMessage(
            messageElement,
            "Unable to connect to the backend. Please try again.",
            "error"
        );

    }

}


// =========================================================
// MESSAGE HELPER
// =========================================================

function showMessage(
    element,
    message,
    type
) {

    if (!element) {

        console.log(
            `[${type}] ${message}`
        );

        return;

    }


    element.textContent =
        message;


    element.className =
        "auth-message";


    if (type === "error") {

        element.classList.add(
            "error"
        );

    }


    if (type === "success") {

        element.classList.add(
            "success"
        );

    }


    if (type === "loading") {

        element.classList.add(
            "loading"
        );

    }

}


// =========================================================
// LOGOUT
// =========================================================

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "user_email"
    );


    window.location.href =
        "index.html";

}


// =========================================================
// GET SAVED TOKEN
// =========================================================

function getToken() {

    return localStorage.getItem(
        "access_token"
    );

}


// =========================================================
// AUTHORIZATION HEADERS
// =========================================================

function apiHeaders() {

    const token =
        getToken();


    return {

        "Content-Type":
            "application/json",

        "Authorization":
            `Bearer ${token}`

    };

}


// =========================================================
// CHECK LOGIN STATUS
// =========================================================

function isLoggedIn() {

    const token =
        getToken();


    return Boolean(token);

}


// =========================================================
// AUTO INITIALIZATION
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "AI Business Agent frontend loaded."
        );

        console.log(
            "Backend:",
            BACKEND_URL
        );

    }
);

const BACKEND_URL =
    "https://ai-business-agent-sm7c.vercel.app";
    
function showLogin() {
    const loginSection = document.getElementById("loginSection");
    const registerSection = document.getElementById("registerSection");
    const loginTab = document.getElementById("loginTab");
    const registerTab = document.getElementById("registerTab");

    if (!loginSection || !registerSection) {
        console.error("Login/Register sections not found.");
        return;
    }

    loginSection.classList.remove("hidden");
    registerSection.classList.add("hidden");

    if (loginTab) loginTab.classList.add("active");
    if (registerTab) registerTab.classList.remove("active");
}

function showRegister() {
    const loginSection = document.getElementById("loginSection");
    const registerSection = document.getElementById("registerSection");
    const loginTab = document.getElementById("loginTab");
    const registerTab = document.getElementById("registerTab");

    if (!loginSection || !registerSection) {
        console.error("Login/Register sections not found.");
        return;
    }

    registerSection.classList.remove("hidden");
    loginSection.classList.add("hidden");

    if (registerTab) registerTab.classList.add("active");
    if (loginTab) loginTab.classList.remove("active");
}

async function getApiError(response, defaultMessage) {
    try {
        const data = await response.json();
        return data.detail || data.message || defaultMessage;
    } catch (error) {
        return response.statusText || defaultMessage;
    }
}

function showMessage(element, message, type) {
    if (!element) {
        console.log(`[${type}] ${message}`);
        return;
    }

    element.textContent = message;
    element.className = "auth-message";

    if (type === "error") element.classList.add("error");
    if (type === "success") element.classList.add("success");
    if (type === "loading") element.classList.add("loading");
}

async function loginUser(event) {
    if (event) event.preventDefault();

    const emailInput = document.getElementById("loginEmail");
    const passwordInput = document.getElementById("loginPassword");
    const messageElement = document.getElementById("loginMessage");

    if (!emailInput || !passwordInput) {
        console.error("Login input elements not found.");
        return;
    }

    const email = emailInput.value.trim().toLowerCase();
    const password = passwordInput.value;

    if (!email) {
        showMessage(messageElement, "Please enter your email.", "error");
        return;
    }

    if (!password) {
        showMessage(messageElement, "Please enter your password.", "error");
        return;
    }

    showMessage(messageElement, "Signing in...", "loading");

    try {
        const response = await fetch(`${BACKEND_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (!response.ok) {
            const errorMessage = await getApiError(
                response,
                "Invalid email or password."
            );

            showMessage(messageElement, errorMessage, "error");
            return;
        }

        const data = await response.json();

        console.log("LOGIN RESPONSE:", data);

        if (!data.access_token) {
            showMessage(
                messageElement,
                "Login succeeded, but no access token was received.",
                "error"
            );
            return;
        }

        localStorage.setItem(
            "access_token",
            data.access_token
        );

        localStorage.setItem(
            "user_email",
            email
        );

        showMessage(
            messageElement,
            "Login successful. Opening dashboard...",
            "success"
        );

        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 700);

    } catch (error) {
        console.error("LOGIN ERROR:", error);

        showMessage(
            messageElement,
            "Unable to connect to the backend. Please try again.",
            "error"
        );
    }
}

async function registerUser(event) {
    if (event) event.preventDefault();

    const nameInput = document.getElementById("registerName");
    const businessInput = document.getElementById("registerBusiness");
    const emailInput = document.getElementById("registerEmail");
    const phoneInput = document.getElementById("registerPhone");
    const passwordInput = document.getElementById("registerPassword");
    const messageElement = document.getElementById("registerMessage");

    if (!nameInput || !businessInput || !emailInput || !passwordInput) {
        console.error("Registration input elements not found.");
        return;
    }

    const name = nameInput.value.trim();
    const businessName = businessInput.value.trim();
    const email = emailInput.value.trim().toLowerCase();
    const phone = phoneInput
        ? phoneInput.value.trim()
        : "";
    const password = passwordInput.value;

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

    showMessage(
        messageElement,
        "Creating your account...",
        "loading"
    );

    try {
        const response = await fetch(
            `${BACKEND_URL}/register`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
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

        if (!response.ok) {
            const errorMessage = await getApiError(
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

        const data = await response.json();

        console.log(
            "REGISTER RESPONSE:",
            data
        );

        showMessage(
            messageElement,
            "Account created successfully. Please login.",
            "success"
        );

        nameInput.value = "";
        businessInput.value = "";
        emailInput.value = "";

        if (phoneInput) {
            phoneInput.value = "";
        }

        passwordInput.value = "";

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

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");

    window.location.href = "index.html";
}

function getToken() {
    return localStorage.getItem("access_token");
}

function apiHeaders() {
    const token = getToken();

    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

function isLoggedIn() {
    return Boolean(getToken());
}

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

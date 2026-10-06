// =========================================
// BACKEND CONFIGURATION
// =========================================

const BACKEND_URL = "https://ai-business-agent-iga7qjvqc-sameerbhorania486.vercel.app";

// =========================================
// TAB SWITCHING
// =========================================

function showLogin() {

    document
        .getElementById("loginForm")
        .classList.remove("hidden");

    document
        .getElementById("registerForm")
        .classList.add("hidden");

    document
        .getElementById("loginTab")
        .classList.add("active");

    document
        .getElementById("registerTab")
        .classList.remove("active");
}


function showRegister() {

    document
        .getElementById("registerForm")
        .classList.remove("hidden");

    document
        .getElementById("loginForm")
        .classList.add("hidden");

    document
        .getElementById("registerTab")
        .classList.add("active");

    document
        .getElementById("loginTab")
        .classList.remove("active");
}


// =========================================
// MESSAGE HELPER
// =========================================

function showMessage(
    elementId,
    message,
    type
) {

    const element =
        document.getElementById(elementId);

    element.textContent = message;

    element.className =
        `message ${type}`;
}


// =========================================
// LOGIN
// =========================================

async function loginUser() {

    const email =
        document
            .getElementById("loginEmail")
            .value
            .trim()
            .toLowerCase();

    const password =
        document
            .getElementById("loginPassword")
            .value;


    if (!email || !password) {

        showMessage(
            "loginMessage",
            "Please enter your email and password.",
            "error"
        );

        return;
    }


    try {

        showMessage(
            "loginMessage",
            "Signing in...",
            "success"
        );


        const response =
            await fetch(
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


        const data =
            await response.json();

            console.log("REGISTER RESPONSE:", data);

        if (!response.ok) {

            const errorMessage =
                data.detail ||
                data.message ||
                "Login failed.";

            showMessage(
                "loginMessage",
                errorMessage,
                "error"
            );

            return;
        }


        if (!data.access_token) {

            showMessage(
                "loginMessage",
                "Login succeeded but no access token was returned.",
                "error"
            );

            return;
        }


        // -----------------------------------------
        // SAVE JWT TOKEN
        // -----------------------------------------

        localStorage.setItem(
            "access_token",
            data.access_token
        );


        // -----------------------------------------
        // SAVE USER EMAIL
        // -----------------------------------------

        localStorage.setItem(
            "user_email",
            email
        );


        showMessage(
            "loginMessage",
            "Login successful. Redirecting...",
            "success"
        );


        // -----------------------------------------
        // TEMPORARY DASHBOARD REDIRECT
        // -----------------------------------------

        setTimeout(
            () => {

               window.location.href = "dashboard.html";

            },
            700
        );

    }

    catch (error) {

        console.error(error);

        showMessage(
            "loginMessage",
            "Unable to connect to backend.",
            "error"
        );
    }
}


// =========================================
// REGISTER
// =========================================

async function registerUser() {

    const name =
        document
            .getElementById("registerName")
            .value
            .trim();


    const businessName =
        document
            .getElementById("businessName")
            .value
            .trim();


    const email =
        document
            .getElementById("registerEmail")
            .value
            .trim()
            .toLowerCase();


    const phone =
        document
            .getElementById("registerPhone")
            .value
            .trim();


    const password =
        document
            .getElementById("registerPassword")
            .value;


    if (!name) {

        showMessage(
            "registerMessage",
            "Please enter owner name.",
            "error"
        );

        return;
    }


    if (!businessName) {

        showMessage(
            "registerMessage",
            "Please enter business name.",
            "error"
        );

        return;
    }


    if (!email) {

        showMessage(
            "registerMessage",
            "Please enter email.",
            "error"
        );

        return;
    }


    if (!password) {

        showMessage(
            "registerMessage",
            "Please create a password.",
            "error"
        );

        return;
    }


    try {

        showMessage(
            "registerMessage",
            "Creating your account...",
            "success"
        );


        const response =
            await fetch(
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

                        business_name:
                            businessName,

                        phone: phone

                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            const errorMessage =
                data.detail ||
                data.message ||
                "Registration failed.";

            showMessage(
                "registerMessage",
                errorMessage,
                "error"
            );

            return;
        }


        showMessage(
            "registerMessage",
            "Account created successfully. You can now login.",
            "success"
        );


        // -----------------------------------------
        // CLEAR FORM
        // -----------------------------------------

        document
            .getElementById("registerName")
            .value = "";

        document
            .getElementById("businessName")
            .value = "";

        document
            .getElementById("registerEmail")
            .value = "";

        document
            .getElementById("registerPhone")
            .value = "";

        document
            .getElementById("registerPassword")
            .value = "";


        // -----------------------------------------
        // SWITCH TO LOGIN
        // -----------------------------------------

        setTimeout(
            () => {

                showLogin();

            },
            1200
        );

    }

    catch (error) {

        console.error(error);

        showMessage(
            "registerMessage",
            "Unable to connect to backend.",
            "error"
        );
    }
}
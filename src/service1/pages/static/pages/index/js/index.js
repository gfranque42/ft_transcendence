
// Import the Home view class
import Home from "../views/home.js";
import Login from "../views/login.js";
import Register from "../views/register.js";
import csrfToken from "../views/register.js";


// Define a function to convert path to regex
const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

// Function to extract parameters from a match
const getParams = match => {
    const values = match.result.slice(1);
    const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

    return Object.fromEntries(keys.map((key, i) => {
        return [key, values[i]];
    }));
};

// Function to navigate to a URL
const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

// Router function
const router = async () => {
    // Define routes
    console.log("Router function called");
    const routes = [
        { path: "/", view: Home },
        { path: "/login/", view: Login },
        { path: "/register/", view: Register }
        // { path: "/signup/", view: () => console.log("Viewing signup")},
    ];

    // Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            result: location.pathname.match(pathToRegex(route.path))
        };
    });

    // Find the first matching route
    let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);

    // If no match found, default to the first route
    if (!match) {
        match = {
            route: routes[0],
            result: [location.pathname]
        };
    }

    // Instantiate the view and render it
    const view = new match.route.view(getParams(match));
    document.documentElement.innerHTML = await view.getHtml();

    if (match.route.path == "/register/") {
        console.log("post awaited");
        const registrationForm = document.querySelector('form.form-register');
        registrationForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const username = document.querySelector('input[name="username"]');
            const password1 = document.querySelector('input[name="password1"]');
            const password2 = document.querySelector('input[name="password2"]');
            let data = view.registerUser(username, password1, password2)
            console.log(data);
            // navigateTo("/");
        });

    } else {
        console.log("nothing to post");
    }
};

// Listen for popstate event and trigger router
window.addEventListener("popstate", router);

// Listen for DOMContentLoaded event and trigger router
document.addEventListener("DOMContentLoaded", () => {
    // Listen for click events on elements with data-link attribute
    document.body.addEventListener("click", e => {
        if (e.target.closest("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }
    });

    // Initial router call
    router();
});

// import RegisterView from "./registerview.js";

// Create an instance of the RegisterView class
// const registerView = new RegisterView();

// // Call the getHtml method to retrieve the HTML content and CSRF token
// registerView.getHtml().then(({ tempContentHtml }) => {
//     // Append the HTML content to the body of the page
//     document.body.innerHTML = tempContentHtml;

//     // Add event listener to the registration form
//     const registrationForm = document.querySelector('#registration-form');
//     registrationForm.addEventListener('submit', async (event) => {
//         event.preventDefault();

//         // Get the username and password from the form
//         const username = document.querySelector('#username').value;
//         const password = document.querySelector('#password').value;

//         // Call the registerUser method to register the user
//         const response = await registerView.registerUser(username, password);

//         // Handle the response
//         if (response.success) {
//             console.log('User registered successfully');
//             navigateTo('/');
//         } else {
//             console.error('Registration failed:', response.error);
//         }
//     });
// });

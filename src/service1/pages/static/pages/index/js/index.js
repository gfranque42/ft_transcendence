
// Import the Home view class
import Home from "../views/home.js";
import Login from "../views/login.js";
import Register from "../views/register.js";

import {setCookie, getCookie, eraseCookie} from "./cookie.js";

let UserToken = null;

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
            UserToken = view.registerUser(username, password1, password2);
            navigateTo("/");
        });
    } else if (match.route.path == "/login/") {
        console.log("post awaited");
        const loginForm = document.querySelector('form.form-login');
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const username = document.querySelector('input[name="username"]');
            const password = document.querySelector('input[name="password"]');
            UserToken = view.loginUser(username, password);
            navigateTo("/");
        });
    }
    console.log(UserToken);
    if (!UserToken)
    {
        UserToken = getCookie("token");
        console.log(UserToken);
    }
    displayUser();
};

async function getToken() {
    // Simulating an async operation to get a token
    return UserToken; // Replace with actual logic
}

async function displayUser()
{
    let tempToken = await getToken();

    if (!tempToken) 
        return ;

    setCookie("token", tempToken, 42)
    console.log(tempToken);
    const options = {
        method: 'GET', // HTTP method
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${tempToken}`
        }
        
    };

    const response = await fetch('http://localhost:8000/auth/test_token', options);
    const UserInformation = await response.json();
    console.log(UserInformation);
    document.getElementById('user').textContent = UserInformation.Username;


}

// Listen for popstate event and trigger router
window.addEventListener("popstate", router);

// Listen for DOMContentLoaded event and trigger router
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");


    document.addEventListener('click', function(event) {
        if (event.target.matches('a[data-link]')) {
            event.preventDefault();
            console.log('Clicked on a link with data-link attribute');
            // Perform your navigation or other actions here
            navigateTo(event.target);
        }
    });
    console.log("Initial router call");
    router();
});

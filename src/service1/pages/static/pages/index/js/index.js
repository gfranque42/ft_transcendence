
// Import the Home view class
import Home from "../views/home.js";
import Login from "../views/login.js";
import Register from "../views/register.js";
import Sudoku from "../views/sudoku.js";
import SudokuLobby from "../views/lobby_sudoku.js";
import SudokuWaiting from "../views/waiting_sudoku.js";


import { initialize } from "./sudoku/sudoku.js";
import {setBoard} from "./sudoku/board.js";
import { PvP, Solo, Start, Easy, Medium, Hard, changeUsername } from "./sudoku/lobby.js";

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

function JSONItirator(FullForm) {
    const form =  FullForm.form;
    const valuesArray = [];

    for(const key in form) {
        for (const value in form[key]) {
            valuesArray.push(form[key][value]);
        }        
    }

    const errorElements = document.querySelectorAll(".error");

    if (errorElements.length === 1) {
        errorElements[0].textContent = "Incorrect username or password";
        return ;
    }

    errorElements.forEach((element, index) => {
        if (valuesArray[index])
            element.textContent = valuesArray[index];
        else
            element.textContent = "";
    });
    
}

// Router function
const router = async () => {
    // Define routes
    console.log("Router function called");
    const routes = [
        { path: "/", view: Home },
        { path: "/login/", view: Login },
        { path: "/register/", view: Register },
        { path: "/sudoku/", view: Sudoku },
        { path: "/sudoku/waiting-room", view: SudokuWaiting },
		{ path: '/sudoku/[A-Za-z0-9]{10}/', view: SudokuLobby }
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
	console.log("potentialMatches: ", potentialMatches);

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
    
    async function checkForm(form) {
        const FullForm = await form;
        if (FullForm)
            JSONItirator(FullForm);
        if (FullForm.token)
            return await FullForm.token;
        return await null;
    }

    async function navigateAfterPost(UserToken) {
        // console.log("UserToken: ", UserToken.form);
        const token = await UserToken;
        if (token)
            navigateTo("/");
    }

    if (match.route.path == "/register/") {
        console.log("post awaited");
        const registrationForm = document.querySelector('form.form-register');
        registrationForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const username = document.querySelector('input[name="username"]');
            const password1 = document.querySelector('input[name="password1"]');
            const password2 = document.querySelector('input[name="password2"]');
            UserToken = checkForm(view.registerUser(username, password1, password2));

            navigateAfterPost(UserToken);
        });
    } else if (match.route.path == "/login/") {
        console.log("post awaited");
        const loginForm = document.querySelector('form.form-login');
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            
            const username = document.querySelector('input[name="username"]');
            const password = document.querySelector('input[name="password"]');
            UserToken = checkForm(view.loginUser(username, password));
            // checkForm(form)
            navigateAfterPost(UserToken);
        });
    } else if (match.route.path == "/sudoku/") {
        console.log("post awaited");

		const actionHandlers = {
			PvP: PvP,
			Solo: Solo,
			Start: Start,
			Easy: Easy,
			Medium: Medium,
			Hard: Hard,
			Start: Start,
		};

		changeUsername(view);
		document.addEventListener('click', function(event) {
			// Handling data-action for button actions
			const action = event.target.getAttribute('data-action');
			if (action && actionHandlers[action]) {
				actionHandlers[action](view); // Call the corresponding function from the lookup table
			} else if (action) {
				console.warn('No action defined for', action);
			}
		});
    } else if (match.route.path == '/sudoku/[A-Za-z0-9]{10}/') {
		setBoard();
		initialize();
	}
    if (!UserToken)
            UserToken = getCookie("token");
	displayUser();
    
    
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
    const options = {
        method: 'GET', // HTTP method
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${tempToken}`
        }
        
    };

    const response = await fetch('https://localhost:8083/auth/test_token', options);
    if (!response.ok)
    {
        eraseCookie("token");
        return ;
    }
    const UserInformation = await response.json();
    let user = document.getElementById('user')
	if (user)
	{
		user.outerHTML = `<div class="navbar-content user-present" id="user">${UserInformation.Username}
        <div class="art-marg"></div>
        <div class="disconnect" id="disconnect">Log out</div>
    	</div>`;
	}
}}

// Listen for popstate event and trigger router
window.addEventListener("popstate", router);

// Listen for DOMContentLoaded event and trigger router
document.addEventListener("DOMContentLoaded", () => {
    


    document.addEventListener('click', function(event) {
		
        if (event.target.matches('a[data-link]')) {
            event.preventDefault();
            navigateTo(event.target);
        }
    });
    document.addEventListener("click", function(event) {
        const UserTest = document.querySelector(".navbar-content.user-present")
        if (event.target.matches('#disconnect'))
        {
            eraseCookie("token");
            UserToken = null;
            document.getElementById('user').outerHTML = '<a href="/register/" class="navbar-content" id="user" data-link>REGISTER</a>';
        }
    });
    router();
});

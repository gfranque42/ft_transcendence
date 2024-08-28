
// Import the Home view class
import Home from "../views/home.js";
import Login from "../views/login.js";
import Verification from "../views/Verification.js";
import Register from "../views/register.js";
import Profile from "../views/profile.js";

import {setCookie, getCookie, eraseCookie} from "./cookie.js";

let UserToken = null;

// Define a function to convert path to regex
const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const getParams = match => {
    const values = match.result.slice(1);
    const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

    return Object.fromEntries(keys.map((key, i) => {
        return [key, values[i]];
    }));
};

// Function to navigate to a URL
export const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

function JSONItirator(form) {
    // console.log(form);
    const valuesArray = [];

    
    for(const key in form) {
        for (const value in form[key]) {
            valuesArray.push(form[key][value]);
        }        
    }
    
    const errorElements = document.querySelectorAll(".error");
    console.log(errorElements);
    
    if (form.detail == "Username is taken") {
        errorElements[0].textContent = form.detail;
        return ;        
    }
    if (errorElements.length === 1 && form.detail) {

        errorElements[0].textContent = "Incorrect username or password";
        return ;
    } else if (errorElements.length === 1)
        return ;
    
    
    errorElements.forEach((element, index) => {
        if (valuesArray[index])
            element.textContent = valuesArray[index];
        else
        element.textContent = "";
});

}
async function navigateAfterPost(UserToken) {
    const token = await UserToken;

    if (token)
        navigateTo("/");
}

async function checkOTP(status, token) {
    const tmp = await status;
    if (tmp.error)
    {
        const errorElements = document.querySelector(".error");
        errorElements.innerHTML = "Invalide verification code";
        return false;
    }
    UserToken = token;
    navigateAfterPost(UserToken);
    return true;
}

function VerificationEvent(verification, token) {
    document.addEventListener('submit', function(event){
        event.preventDefault();
        if (event.target.id == 'form-otp') {
            console.log("VerificationForm: ", event.target);
            const otp = document.querySelector('input[name="otp"]');
            const status = verification.verifactionUser(otp, token);
            return checkOTP(status, token);
        }
    });
}

function hidePopstate() {
    var qrCode = document.getElementById('qr-code');
    var emailCode = document.getElementById('email-code');
    var smsCode = document.getElementById('sms-code');
    var clickOff = document.getElementById('click-off');

    qrCode.style.display = 'none';
    emailCode.style.display = 'none';
    smsCode.style.display = 'none';
    clickOff.style.filter = 'none';
}


const router = async () => {
    console.log("Router function called");
    const routes = [
        { path: "/", view: Home },
        { path: "/login/", view: Login },
        { path: "/profile/", view: Profile },
        { path: "/register/", view: Register }
        // { path: "/signup/", view: () => console.log("Viewing signup")},
    ];
    
    
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            result: location.pathname.match(pathToRegex(route.path))
        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);

    if (!match) {
        match = {
            route: routes[0],
            result: [location.pathname]
        };
    }
    
    const view = new match.route.view(getParams(match));
    document.documentElement.innerHTML = await view.getHtml();
    
    async function checkForm(form) {
        const FullForm = await form;
        if (FullForm)
            JSONItirator(FullForm);
        // console.log("form has been ititrated");
        if (FullForm.token)
            return FullForm.token;
        if (FullForm.Success)
            return true;
        return null;
    }
    
    async function navigateToOTP(verification, token) {
        const otptoken = await token;
        if (otptoken) {
            if (otptoken)
                return 2
            document.documentElement.innerHTML = await verification.getHtml(otptoken);
            return 1
        }
        return 3;
    }
    
    async function VerificationRoute(tempToken) {
        const verification = new Verification();
        const token = await tempToken;
        if (token === null)
            return ;
        UserToken = null;
        const navStatus = await navigateToOTP(verification, token);
        if (navStatus == 1) {
            if (VerificationEvent(verification, token));
                return ;
        }
        else if (navStatus == 2) {
            UserToken = token
            navigateAfterPost(token);
            return ;
        }
        VerificationRoute();
    }

    async function FollowingProfile(TmpIsCorrect) {
        const IsCorrect = await TmpIsCorrect;
        if (IsCorrect)
            navigateTo("/profile/")

    } 

    if (!UserToken)
        UserToken = getCookie("token");

    if (match.route.path == "/register/") {
        console.log("post awaited");
        const registrationForm = document.querySelector('form.form-register');
        registrationForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const email = document.querySelector('input[name="email"]');
            const username = document.querySelector('input[name="username"]');
            const password1 = document.querySelector('input[name="password1"]');
            const password2 = document.querySelector('input[name="password2"]');
            UserToken = checkForm(view.registerUser(email, username, password1, password2));
            navigateAfterPost(UserToken);
        });
    } else if (match.route.path == "/login/") {
        console.log("post awaited");
        const loginForm = document.querySelector('form.form-login');
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.querySelector('input[name="username"]');
            
            const password = document.querySelector('input[name="password"]');
            VerificationRoute(checkForm(view.loginUser(username, password)));
        });
    } else if (match.route.path == "/profile/") {
        console.log("post awaited profile");
        const profileForm = document.querySelectorAll('form');
        profileForm.forEach((form) => {
            form.addEventListener('submit', (event) => {
                event.preventDefault();
                const username = document.querySelector('input[name="username"]');
                const avatar = document.querySelector('input[name="avatar"]');
                if (username.value || avatar.value) {
                    FollowingProfile(checkForm(view.profileUserPatch(UserToken, username, avatar)))
                } else {
                    const email = document.querySelector('input[name="email"]');
                    const sms = document.querySelector('input[name="sms"]');
                    const otp = document.querySelector('input[name="otp"]');
                    console.log(email);
                    console.log(sms);
                    console.log(otp);
                    // console.log(email);
                    // profileUserPost(UserToken, email, sms, otp)
                    const verif = view.profileUserPost(UserToken, email, sms, otp);
                    const isOkay = FollowingProfile(checkForm(verif));
                    if (isOkay) {
                        LastCheckAddVerification(view.profileUserPost(UserToken, email, sms, otp), UserToken);
                    } else {
                        console.log("is not okay") // add to this
                    }

                }
            });
            
            // checkForm(form)
            // navigateAfterPost(UserToken);

        });
    }

    if (!UserToken)
            UserToken = getCookie("token");
        displayUser();
    };
    
    
    async function getToken() {
        return UserToken;
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

    const response = await fetch('http://localhost:8000/auth/test_token', options);
    if (!response.ok)
    {
        eraseCookie("token");
        return ;
    }
    const UserInformation = await response.json();
    document.getElementById('user').outerHTML = `<div class="navbar-content user-present" id="user">${UserInformation.Username}
        <div class="art-marg"></div>
        <div class="disconnect" id="disconnect">Log out</div>
    </div>`;
}

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
    document.addEventListener('click', function(event) {
        // Get references to the elements
        var qrCode = document.getElementById('qr-code');
        var emailCode = document.getElementById('email-code');
        var smsCode = document.getElementById('sms-code');
        var clickOff = document.getElementById('click-off');
        var popup = document.querySelectorAll('#simple-popup');
        const ispopup = Array.from(popup).some(div =>  div.contains(event.target));

        !(event.target.matches('.popup'))
        if (event.target.matches('#setup-email')) {
            emailCode.style.display = 'block';
            clickOff.style.filter = 'blur(5px)';
        } else if (event.target.matches('#setup-sms')) {
            smsCode.style.display = 'block';
            clickOff.style.filter = 'blur(5px)';
        } else if (event.target.matches('#setup-app')) {
            qrCode.style.display = 'block';
            clickOff.style.filter = 'blur(5px)';
        } else if (!ispopup) {
            hidePopstate();
        }

    });
    router();
});

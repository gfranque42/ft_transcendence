
// Import the Home view class
import Home from "../views/home.js";
import Login from "../views/login.js";
import Verification from "../views/Verification.js";
import Register from "../views/register.js";
import Pong from "../views/pong.js";
import PongLobby from "../views/pong_lobby.js";
import {vec2, paddle, ball, game, waitForSocketConnection, wsonmessage} from  "../pong/pong.js";
import {eventPong, checkConnection} from "../pong/index.js";
import Profile from "../views/profile.js";
import Sudoku from "../views/sudoku.js";
import SudokuLobby from "../views/lobby_sudoku.js";
import SudokuWaiting from "../views/waiting_sudoku.js";

import { initialize } from "./sudoku/sudoku.js";
import { PvP, Solo, Start, Easy, Medium, Hard, changeUsername } from "./sudoku/lobby.js";

import {getRenewedToken} from "./token.js"
import {logout} from "./logout.js"
import {setCookie, getCookie, eraseCookie} from "./cookie.js";

let UserToken = null;
var isLoaded = false;
// var view = null;

function isEmptyOrWhitespace(str) {
    return !str || /^\s*$/.test(str);
}


window.addEventListener('beforeunload', function (event) {
    console.log("UNLOADING");
    logout(UserToken);
});

export let myGame = new game(new paddle(new vec2(-2, -2), new vec2(1, 1)), new paddle(new vec2(-2, -2), new vec2(1, 1)), new ball(new vec2(-2, -2), new vec2(1, 1), new vec2(0, 0)));

// Define a function to convert path to regex
const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const getParams = match => {
	const values = match.result.slice(1);
	const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

	return Object.fromEntries(keys.map((key, i) => {
		return [key, values[i]];
	}));
};

export const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

export const navigateToInstead = url => {
    history.replaceState(null, null, url);
    router();
};

function JSONItirator(form) {
    const valuesArray = [];
    
    console.log(form);

    if (form.success)
        return;
    for(const key in form) {
        for (const value in form[key]) {
            // if (value)
            if (value === 'password2') 
            {
                for (const item in form[key][value])
                    valuesArray.push(form[key][value][item]);
            } else
                valuesArray.push(form[key][value]);
        }        
    }
    
    const errorElements = document.querySelectorAll(".error");
    
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
        {
            console.log(typeof(valuesArray[index]));
            element.textContent = valuesArray[index];
        }
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
    // console.log("verification event");
    document.addEventListener('submit', function(event){
        event.preventDefault();
        if (event.target.id == 'form-otp') {
            // console.log("VerificationForm: ", event.target);
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
    var friendRequest = document.getElementById('friend-request-code');
    var clickOff = document.getElementById('click-off');

    if (qrCode) qrCode.style.display = 'none';
    if (emailCode) emailCode.style.display = 'none';
    if (smsCode) smsCode.style.display = 'none';
    if (friendRequest) friendRequest.style.display = 'none';
    if (clickOff) clickOff.style.filter = 'none';
}


const router = async () => {
  
    ("Router function called");
    const routes = [
        { path: "/", view: Home },
        { path: "/login/", view: Login },
        { path: "/profile/", view: Profile },
        { path: "/register/", view: Register },
        { path: "/sudoku/", view: Sudoku },
        { path: "/sudoku/waiting-room", view: SudokuWaiting },
		    { path: '/sudoku/[A-Za-z0-9]{10}/', view: SudokuLobby },
		    { path: "/pong/", view: Pong },
		    { path: '/pong/[A-Za-z0-9]{10}/', view: PongLobby }
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
        if (FullForm.token)
            return FullForm.token;
        if (FullForm.success)
            return true;
        return null;
    }

    async function navigateToOTP(verification, token) {
        const otptoken = await token;
        if (otptoken) {
            const sendableCode = await verification.isVerification(token);
            if (!sendableCode.method)
                return 2
            document.documentElement.innerHTML = await verification.getHtml(otptoken);
            return 1
        }
        return 3;
    }

    async function friendRequestCheck(data) {
        hidePopstate();
        if (data.success) {
            alert(await data.success);
        }
    }

    async function VerificationRoute(tempToken) {
        const verification = new Verification();
        const token = await tempToken;
        if (token === null)
            return ;
        const navStatus = await navigateToOTP(verification, token);
        UserToken = token
        if (navStatus == 1) {
            if (VerificationEvent(verification, token));
            return ;
        }
        else if (navStatus == 2) {
            navigateAfterPost(token);
            return ;
        }
        UserToken = null;
        VerificationRoute();
    }

    async function awaitSuccess(verif) {
        return await verif.success;
    }

    async function FollowingProfile(TmpIsCorrect, verif) {
        const IsCorrect = await TmpIsCorrect;
        const isOTP = await verif;

        if (IsCorrect)
        {
            // console.log(isOTP);
            if (isOTP && isOTP.otp)
                navigateTo("/profile/")
            return true;
        }
        return false;
    }

    async function profileUtils(verif, isOkay) {
        const check_otp = await verif;
        const check_form = await isOkay;

        if (check_otp.otp || check_form)
        {
            // console.log(check_otp.otp, check_form);
            navigateTo("/profile/")
            return ;
        }
        
        console.log(check_otp, check_form);
        hidePopstate();
        const otpPopup = document.getElementById('profile-otp-code');
        const clickOff = document.getElementById('click-off');

        otpPopup.style.display = 'block';
        clickOff.style.filter = 'blur(5px)';
        // }
    }


    if (!UserToken) {
        const token = getCookie("token")
            
        if (token != null)
            UserToken = getRenewedToken(token)
    }
    if (match.route.path == "/") {
        if (isLoaded)
            document.querySelector('#app').style.display = 'block';
    }
    else if (match.route.path == "/register/") {
                                                                            // REGISTER     It send the information given by the user to the authapi and adds a cookie
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
                                                                            // LOGIN    sends credentials to authapi, and gets verification if user has verification finally sends the code inpiuted by the user also adds a cookie with token

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
                const formElement = event.target;
                const accept = formElement.querySelector('#reject');
                const username = document.querySelector('input[name="username"]');
                const avatar = document.querySelector('input[name="avatar"]');
                const to_user = document.querySelector('input[name="to_user"]');
                if ('btn-profile-update' == event.submitter.id) {
                    FollowingProfile(checkForm(view.profileUserPatch(UserToken, username, avatar)))
                } else if (event.submitter.id == 'accept' || event.submitter.id == 'reject') {
                    if (event.submitter.id == 'accept')
                        FollowingProfile(view.friendRequest(UserToken, true,  event.submitter.value))
                    else
                        FollowingProfile(view.friendRequest(UserToken, false,  event.submitter.value))
                } else if (event.submitter.id == 'friend-form') {
                    friendRequestCheck(view.sendFriendRequest(UserToken, to_user));
                } else if (event.submitter.id == 'unfriend') {
                    FollowingProfile(view.deleteFriend(UserToken, event.submitter));
                    navigateTo("/profile/")
                } else {
                    const email = document.querySelector('input[name="email"]');
                    const phone_number = document.querySelector('input[name="phone_number"]');
                    const otp = document.querySelector('input[name="otp"]');
                    const app = document.querySelector('input[name="app"]');

                    const verif = view.profileUserPost(UserToken, email, phone_number, otp, app);
                    const isOkay = FollowingProfile(awaitSuccess(verif), verif);
                    profileUtils(verif, isOkay);
                    // const otpPopup = document.getElementById('profile-otp-code');
                }
            });
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
		initialize();
	} else if (match.route.path == "/pong/") {
		await checkConnection();
		eventPong(view);

	} else if (match.route.path == "/pong/[A-Za-z0-9]{10}/") {
		await checkConnection();
		var socketProtocol = 'ws://';
		console.log(window.location.protocol);
		if (window.location.protocol === 'https:')
		{
			console.log('protocol https');
			socketProtocol = 'wss://';
		}

		const roomSocket = new WebSocket(
			socketProtocol
			+ window.location.host
			+ '/ws'
			+ window.location.pathname
		);
		await waitForSocketConnection(roomSocket);

		console.log('my game is ready: ', myGame.gameState);

		const canvas = document.getElementById('canvas');
		const ctx = canvas.getContext('2d');
		canvas.width = window.innerWidth * 0.8;
		canvas.height = window.innerHeight * 0.7;
		roomSocket.onmessage = function (e)
		{
			const data = JSON.parse(e.data);
			if (data.type === "fin du compte")
			{
				myGame.gameState = "playing";
			}
			wsonmessage(data, roomSocket, canvas, ctx);
		};

		roomSocket.onclose = function (e)
		{
			console.error('Chat socket closed unexpectedly');
		};

		let starttime = Date.now();
		while (myGame.gameState != "end" && match.route.path == "/pong/[A-Za-z0-9]{10}/")
		{	
			let elapstime = Date.now() - starttime;
			console.log("time: ",elapstime);
			if (elapstime > 1000 / 60)
			{
				myGame.draw(canvas, ctx, (Date.now() - myGame.frameTime) / 1000);
				starttime += 1000 / 60;
				console.log(".");
			}
			await new Promise(r => setTimeout(r, 2));
		}
	}

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

    const response = await fetch('https://localhost:8083/auth/test_token', options);
    if (!response.ok)
    {
        eraseCookie("token");
        return ;
    }
    const UserInformation = await response.json();
    const userElement = document.getElementById('user');
    if (userElement) {
        let profileButton = '';
        if (window.location.pathname === '/' || window.location.pathname === '/home/') {
            profileButton = `<div class="profile" id="profile">Profile</div>`;
        }
        userElement.outerHTML = `<div class="navbar-content user-present" id="user">${await UserInformation.Username}
        <div class="art-marg"></div>
        <div class="disconnect" id="disconnect">Log out</div>
        ${profileButton}
    </div>`;
    }
}

// Listen for popstate event and trigger router
window.addEventListener("popstate", router);

// Listen for DOMContentLoaded event and trigger router
document.addEventListener("DOMContentLoaded", () => {
    //Loader
    console.log("DOM loading")

    const handleHomePageLoad = () => {
        console.log("handleHomePageLoad");
            
        setTimeout(function() {
            const app = document.querySelector('#app');
            const loader = document.querySelector('.loader');
            if (app)
                document.querySelector('#app').style.display = 'none';
            if (loader)
                document.querySelector('.loader').style.display = 'block';
            console.log("Display swicthed")
        },40);
        
        
        setTimeout(function() {
            const app = document.querySelector('#app');
            const loader = document.querySelector('.loader');
            console.log("Display swicthed agains")
            if (loader)
                document.querySelector('.loader').style.display = 'none';
            if (app)
                document.querySelector('#app').style.display = 'block';
            isLoaded = true;
        },1000);
    };
    
    handleHomePageLoad();
//fin Loader

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
            UserToken = logout(UserToken);
            if (window.location.pathname === '/')
                {
                    document.getElementById('user').outerHTML = '<a href="/register/" class="navbar-content" id="user" data-link>REGISTER</a>';
                }
                else
                {
                    navigateTo('/');
                }
        } else if (event.target.matches('#profile')) {
            navigateTo('/profile/');
        }
        // Get references to the elements
        var qrCode = document.getElementById('qr-code');
        var emailCode = document.getElementById('email-code');
        var smsCode = document.getElementById('sms-code');
        var clickOff = document.getElementById('click-off');
        var friendRequest = document.getElementById('friend-request-code');
        var popup = document.querySelectorAll('#simple-popup');
        const ispopup = Array.from(popup).some(div =>  div.contains(event.target));

        if (event.target.matches('#setup-email')) {
            emailCode.style.display = 'block';
            clickOff.style.filter = 'blur(5px)';
        } else if (event.target.matches('#setup-sms')) {
            smsCode.style.display = 'block';
            clickOff.style.filter = 'blur(5px)';
        } else if (event.target.matches('#setup-app')) {
            qrCode.style.display = 'flex';
            clickOff.style.filter = 'blur(5px)';
        } else if (event.target.matches('#friend-request')) {
            friendRequest.style.display = 'flex';
            clickOff.style.filter = 'blur(5px)';
        } else if (!ispopup) {
            hidePopstate();
        }

        if (event.target.matches('.code-btn')) {
            const verification = new Verification();
            verification.LastCheckAddVerification(UserToken);
        }
    });
    router();
});

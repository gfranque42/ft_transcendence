import abstractviews from "./abstractviews.js";
import {getCookie} from "../js/cookie.js";
import {navigateTo} from "../js/index.js";

export let csrfToken = null;

function isEmptyOrWhitespace(str) {
    return !str || /^\s*$/.test(str);
}

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Profile");
    }

    async getHtml() 
    {
        const token = getCookie("token")
        
        if (token == null) {
            navigateTo("/login/");
            return ;
        }
        
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        };
        
        const response = await fetch('http://localhost:8082/auth/profile', options);
        const tempContentHtml = await response.text();
        
        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;
        console.log(csrfToken);

        return tempContentHtml;
    }

    async profileUserPatch(token, username, avatar) {
        if (csrfToken === null) {
            throw new Error('CSRF token not available');
        }
        if (username.value || avatar.value)
            console.log('succefull');
        else
            console.log('failed');

        let response = await fetch('http://localhost:8082/auth/profile', {
            method: 'PATCH',
            body: JSON.stringify({ 
                "csrfmiddlewaretoken": csrfToken, 
                "token": token,
                "username": username.value,
                "avatar": avatar.value
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        });
        const data = await response.json();

        console.log(data.error);
        return data;
    }

    async profileUserPost(token, email, sms, otp) {
        console.log(csrfToken);
        if (csrfToken === null) {
            throw new Error('CSRF token not available');
        }

        const body = {};

        // Always include the CSRF token and token
        body["csrfmiddlewaretoken"] = csrfToken;
        body["token"] = token;
        console.log(email.value);
        console.log(sms);

        // Conditionally add properties if they have values
        if (sms !== null && !isEmptyOrWhitespace(sms.value))
            body["sms"] = sms.value;
        if (email !== null && !isEmptyOrWhitespace(email.value))
            body["email"] = email.value;
        if (otp !== null && !isEmptyOrWhitespace(otp.value))
            body["otp"] = otp.value;

        console.log(body);
        // console.log("!",otp.value, " ", isEmptyOrWhitespace(otp),"!");
        let response = await fetch('http://localhost:8082/auth/verification-add', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        });
        const data = await response.json();
        
        console.log(data.error);
        console.log(data);
        return data;
    }
    
    
    async LastCheckAddVerification(Usertoken) { 
        const token = await UserToken;
        
        let response = await fetch('http://localhost:8082/auth/send-otp', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization': `Token ${token}`
            },
        });
        return response;
    }
    


    setTitle(title) {
        document.title = title;
    }
}
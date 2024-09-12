import abstractviews from "./abstractviews.js";
import {getCookie} from "../js/cookie.js";
import {navigateTo} from "../js/index.js";


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
        
        const response = await fetch('https://localhost:8083/auth/profile', options);
        const tempContentHtml = await response.text();
        
        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        this.csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    async profileUserPatch(token, username, avatar) {
        if (this.csrfToken === null) {
            throw new Error('CSRF token not available');
        }

        // const body = {};
        let formdata = new FormData();


        formdata.append('username', username.value);
        formdata.append('avatar', avatar.files[0]);
        formdata.append('token', token);


        // URLSearchParams searchParams = new URLSearchParams(formdata)
        // body["csrfmiddlewaretoken"] = this.csrfToken;
        // body["token"] = token;


        // // Conditionally add properties if they have values
        // if (username !== null && !isEmptyOrWhitespace(username.value))
        //     body["username"] = username.value;
        // if (avatar !== null)
        //     body["avatar"] = avatar.files[0];

        // console.log(body);

        let response = await fetch('https://localhost:8083/auth/profile', {
            method: 'PATCH',
            body: formdata,
            headers: {
                // 'Content-Type': "application/x-www-form-urlencoded",
                'X-CSRFToken': this.csrfToken,
            },
        });
        const data = await response.json();

        return data;
    }

    async profileUserPost(token, email, sms, otp, app) {
        if (this.csrfToken === null) {
            throw new Error('CSRF token not available');
        }

        const body = {};

        // Always include the CSRF token and token
        body["csrfmiddlewaretoken"] = this.csrfToken;
        body["token"] = token;


        // Conditionally add properties if they have values
        if (sms !== null && !isEmptyOrWhitespace(sms.value))
            body["phone_number"] = sms.value;
        if (email !== null && !isEmptyOrWhitespace(email.value))
            body["email"] = email.value;
        if (otp !== null && !isEmptyOrWhitespace(otp.value))
            body["otp"] = otp.value;
        if (app !== null && !isEmptyOrWhitespace(app.value))
            body["app"] = app.value;
        let response = await fetch('https://localhost:8083/auth/verification-add', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
        });
        const data = await response.json();

        return data;
    }

    setTitle(title) {
        document.title = title;
    }
}
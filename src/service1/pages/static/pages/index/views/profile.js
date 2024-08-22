import abstractviews from "./abstractviews.js";
import {getCookie} from "../js/cookie.js";
import {navigateTo} from "../js/index.js";

export let csrfToken = null;

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

        console.log(options);
        const response = await fetch('http://localhost:8082/auth/profile', options);
        console.log("reposne :", response);
        const tempContentHtml = await response.text();

        console.log(tempContentHtml);
        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;
        console.log(csrfToken);

        return tempContentHtml;
    }

    async profileUser(token, username, avatar) {
        console.log(username);
        console.log(avatar);
        console.log(csrfToken);
        if (csrfToken === null) {
            throw new Error('CSRF token not available');
        }
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

        // if (data.form.username)
        console.log(data.error);
        return data;
    }

    setTitle(title) {
        document.title = title;
    }
}
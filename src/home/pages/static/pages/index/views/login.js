import abstractviews from "./abstractviews.js";
import {DNS} from "../js/dns.js";
import {loadCSS} from "../js/loadCSS.js";


export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Login");
    }

    async getHtml() 
    {
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const cssFiles = [
            'https://'+DNS+':8083/auth/static/pages/register/register.css?request_by=Home',
            'https://'+DNS+':8083/auth/static/pages/register/login.css?request_by=Home',
            'https://'+DNS+':8083/auth/static/pages/register/profile.css?request_by=Home',
            'https://'+DNS+':8083/auth/static/pages/register/navbar.css?request_by=Home',
            'https://'+DNS+':8083/auth/static/pages/register/index.css?request_by=Home'
        ];

        cssFiles.forEach(url => loadCSS(url));
        
        const response = await fetch('https://'+DNS+':8083/auth/login?request_by=Home', options);
        const tempContentHtml = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        this.csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    async loginUser(username, password) {

        if (this.csrfToken === null) {
            throw new Error('CSRF token not available');
        }
        let response = await fetch('https://'+DNS+':8083/auth/login?request_by=Home', {
            method: 'POST',
            body: JSON.stringify({ 
                "csrfmiddlewaretoken": this.csrfToken, 
                "username": username.value,
                "password": password.value
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            },
        });

        const data = await response.json();
        return data;
    }

    setTitle(title) {
        document.title = title;
    }
}

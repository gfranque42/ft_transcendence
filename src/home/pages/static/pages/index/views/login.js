import abstractviews from "./abstractviews.js";

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Login");
    }

    async getHtml() 
    {
        const response = await fetch('https://localhost:8083/auth/login');
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
        let response = await fetch('https://localhost:8083/auth/login', {
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
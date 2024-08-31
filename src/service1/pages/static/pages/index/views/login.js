import abstractviews from "./abstractviews.js";

export let csrfToken = null;

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

        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    async loginUser(username, password) {
        if (csrfToken === null) {
            throw new Error('CSRF token not available');
        }
        let response = await fetch('https://localhost:8083/auth/login', {
            method: 'POST',
            body: JSON.stringify({ 
                "csrfmiddlewaretoken": csrfToken, 
                "username": username.value,
                "password": password.value
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        });

        const data = await response.json();
        // if (data.form.username)
        // console.log(data.token);
        return data;
    }

    setTitle(title) {
        document.title = title;
    }
}

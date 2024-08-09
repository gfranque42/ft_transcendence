import abstractviews from "./abstractviews.js";

export let csrfToken = null;

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Verification");
    }

    async getHtml(UserToken) 
    {
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${UserToken}`
            }
            
        };
        const response = await fetch('http://localhost:8082/auth/verification', options);
        const tempContentHtml = await response.text();

        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    async verifactionUser(otp, token) {
        if (csrfToken === null) {
            throw new Error('CSRF token not available');
        }
        let response = await fetch('http://localhost:8082/auth/verification', {
            method: 'POST',
            body: JSON.stringify({ 
                "csrfmiddlewaretoken": csrfToken, 
                "otp": otp.value,
                "token": token
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
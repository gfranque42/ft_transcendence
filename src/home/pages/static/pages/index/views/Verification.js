import abstractviews from "./abstractviews.js";

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
        const response = await fetch('https://localhost:8083/auth/verification', options);
        const tempContentHtml = await response.text();

        // if (tempContentHtml == '{"success":"No Verification"}')
        //     return false
        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        this.csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    async verifactionUser(otp, token) {
        if (this.csrfToken === null) {
            throw new Error('CSRF token not available');
        }
        let response = await fetch('https://localhost:8083/auth/verification', {
            method: 'POST',
            body: JSON.stringify({ 
                "csrfmiddlewaretoken": this.csrfToken, 
                "otp": otp.value,
                "token": token
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            },
        });

        const data = await response.json();

        // if (data.form.username)
        return data;
    }

    async isVerification(token) {
        let response = await fetch('https://localhost:8083/auth/test_OTP', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        });

        const data = await response.json();

        // if (data.form.username)

        return data;
    }

    setTitle(title) {
        document.title = title;
    }
}
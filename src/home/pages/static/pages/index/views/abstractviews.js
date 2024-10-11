import {DNS} from "../js/dns.js";


export default class {
    constructor() {
        this.csrfToken = null;
    }

    async LastCheckAddVerification(tmpToken) { 
        const token = await tmpToken;

        if (!token)
            return false;
        let response = await fetch('https://'+DNS+':8083/auth/send-otp?request_by=Home', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
                'Authorization': `Token ${token}`
            },
        });
        const data = await response.json();

        return data;
    }

    setTitle(title) {
        document.title = title;
    }

    async getHtml() {
        return "";
    }
}

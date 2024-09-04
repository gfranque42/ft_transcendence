export default class {
    constructor() {
        this.csrfToken = null;
    }



    async LastCheckAddVerification(tmpToken) { 
        const token = await tmpToken;

        let response = await fetch('http://localhost:8082/auth/send-otp', {
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

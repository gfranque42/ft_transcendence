import abstractviews from "./abstractviews.js";

export default class extends abstractviews {
    constructor() {
        super();
        this.setTitle("Login");
    }

    async getHtml() {
        // Fetch content HTML from Django view or API
        const response = await fetch('/login');
        const loginContentHtml = await response.text();

        // Return the content HTML
        return loginContentHtml;
    }

    setTitle(title) {
        document.title = title;
    }
}
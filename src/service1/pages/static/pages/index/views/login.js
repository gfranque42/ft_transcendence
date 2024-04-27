import abstractviews from "./abstractviews.js";

export default class extends abstractviews {
    constructor() {
        super();
        this.setTitle("Login");
    }

    async getHtml() {
        return `
            <p>login<p/>
        `;
    }
}
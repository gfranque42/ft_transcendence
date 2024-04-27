import abstractviews from "./abstractviews.js";

export default class extends abstractviews {
    constructor() {
        super();
        this.setTitle("Home");
    }

    async getHtml() {
        return `
            <p>Home<p/>
        `;
    }
}
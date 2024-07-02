import abstractviews from "./abstractviews.js";

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Login");
    }

    async getHtml() 
    {
        const response = await fetch('/login');
        const tempContentHtml = await response.text();
        const tempContainer = document.createElement('div');
        tempContainer.innerHTML = tempContentHtml;
        const loginContentHtml = tempContainer.querySelector('#app').innerHTML;
        return loginContentHtml;
    }

    setTitle(title) {
        document.title = title;
    }
}
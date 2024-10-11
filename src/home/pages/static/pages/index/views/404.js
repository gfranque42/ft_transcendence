
import {DNS} from "../js/dns.js";


export default class {
    constructor() {
        this.setTitle("Home");
    }

    async getHtml() {
        const response = await fetch('/404');
        const tempContentHtml = await response.text();
        // const tempContainer = document.createElement('div');
        // tempContainer.innerHTML = tempContentHtml;
        // const homeContentHtml = tempContainer.querySelector('#app').innerHTML;
        return tempContentHtml;
    }

    setTitle(title) {
        document.title = title;
    }
}
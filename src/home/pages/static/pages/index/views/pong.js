import abstractviews from "./abstractviews.js";
import {Start} from "../pong/index.js";
import {DNS} from "../js/dns.js";

export let csrfToken = null;

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Pong");
    }

    async getHtml() 
    {
        const response = await fetch('https://'+DNS+':8083/api_pong/getindex/' + '?request_by=Home');
        const tempContentHtml = await response.text();

        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    async PongLobbyCreation(gameMode) {
        return (Start(csrfToken, gameMode));
    }

    setTitle(title) {
        document.title = title;
    }
}
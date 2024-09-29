import abstractviews from "./abstractviews.js";

import {setCookie, getCookie, eraseCookie} from "../js/cookie.js";


export let csrfToken = null;

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Sudoku");
    }

    async getHtml() 
    {
        const response = await fetch('https://localhost:8083/sudokubattle/');
        const tempContentHtml = await response.text();

        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    setTitle(title) {
        document.title = title;
    }
}

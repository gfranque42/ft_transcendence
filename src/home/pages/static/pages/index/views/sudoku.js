import abstractviews from "./abstractviews.js";
import {navigateToInstead} from "../js/index.js";
import {DNS} from "../js/dns.js";
import {loadCSS} from "../js/loadCSS.js";

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
        const token = getCookie("token")
        
        if (token == null) {
            navigateToInstead("/login/");
            return ;
        }

        const cssFiles = [ 
            'https://'+DNS+':8083/sudokubattle/static/css/navbar.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/lobby.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/sudoku.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/waiting.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/index.css?request_by=Home',
            // 'https://'+DNS+':8083/sudokubattle/static/css/index.css?request_by=Home'
        ];

        cssFiles.forEach(url => loadCSS(url));

        const response = await fetch('https://'+DNS+':8083/sudokubattle/?request_by=Home');
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

import abstractviews from "./abstractviews.js";
import {navigateToInstead} from "../js/index.js";
import {getCookie} from "../js/cookie.js";
import {DNS} from "../js/dns.js";
import {loadCSS} from "../js/loadCSS.js";

export let csrfToken = null;

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("SudokuLobby");
    }

    async getHtml() 
    {
        const token = getCookie("token")
        
        if (token == null) {
            navigateToInstead("/login/");
            return ;
        }

        const cssFiles = [ 
            'https://'+DNS+':8083/sudokubattle/static/css/lobby.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/navbar.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/sudoku.css?request_by=Home',
            'https://'+DNS+':8083/sudokubattle/static/css/waiting.css?request_by=Home',
        ];

        cssFiles.forEach(url => loadCSS(url));

		console.log("getHtml lobby called");
		const url = location.pathname;
		const bob = url.replace('/sudoku/', '');
		const room_name = bob.replace('/', '');

        const response = await fetch('https://'+DNS+':8083/sudokubattle/' + room_name + '?request_by=Home');
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

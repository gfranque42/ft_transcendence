import abstractviews from "./abstractviews.js";
import {navigateToInstead} from "../js/index.js";
import {DNS} from "../js/dns.js";

export let csrfToken = null;

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("SudokuWaiting");
    }

    async getHtml() 
    {
        const token = getCookie("token")
        
        if (token == null) {
            navigateToInstead("/login/");
            return ;
        }

        const response = await fetch('https://'+DNS+':8083/sudokubattle/api/waiting_room/?request_by=Home');
        const tempContentHtml = await response.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

        return tempContentHtml;
    }

    setTitle(title) {
        document.title = title;
    }
}

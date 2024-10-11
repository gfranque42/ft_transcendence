import {DNS} from "../js/dns.js";


// import abstractviews from "./abstractviews.js";

// export default class extends abstractviews {
//     constructor() {
//         super();
//         this.setTitle("Home");
//     }

//     // async getHtml() {
//     //     return `
//     //         <script src="/static/pages/index/js/hover.js"></script>

//     //         <div class="index-page-layout">
//     //             <div class="index-main-container">
//     //                 <div class="index-game-titles-container" >
//     //                     <a href="/" class="index-game-title index-pong" class="index-game-title index-pong"><img src="/static/pages/PONG.svg" alt="PONG"></a>
//     //                     <a href="/" class="index-game-title index-sudoku" class="index-game-title index-sudoku"><img src="/static/pages/SUDOKU.svg" alt="SODUKU"></a>
//     //                 </div>
//     //                 <div class="index-game-title">
//     //                     <img class=" index-logo" src="/static/pages/Group.svg" alt="Logo">
//     //                 </div>
//     //             </div>
//     //         </div>
//     //     `;
//     // }

//     async getHtml() {
//         const response = await fetch('/');
//         const loginFormHtml = await response.text();
        
//         return loginFormHtml;
//     }
// }

// pages/index/js/home.js

// pages/static/pages/index/js/home.js

export default class {
    constructor() {
        this.setTitle("Home");
    }

    async getHtml() {
        const response = await fetch('/');
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

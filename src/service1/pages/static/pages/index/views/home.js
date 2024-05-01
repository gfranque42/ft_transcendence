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
        // Fetch content HTML from Django view or API
        const response = await fetch('/');
        const homeContentHtml = await response.text();
        console.log("Content fetched:", homeContentHtml);

        
        // Return the content HTML
        console.log("here");
        return homeContentHtml;
    }

    setTitle(title) {
        document.title = title;
    }
}

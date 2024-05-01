
// function include(file) { 
    
    //     var script  = document.createElement('script'); 
    //     script.src  = file; 
    //     script.type = 'text/javascript'; 
    //     script.defer = true; 
    
    //     document.getElementsByTagName('head').item(0).appendChild(script); 
    
    // } 
    
    // const navigateTo = url => {
        //     history.pushState(null, null, url);
        //     router();
        // };
        
        
        // const router = async () => {
            //     const routes = [
                //         { path: "/", view: () => Home},
                //         // { path: "/login/", view: () => console.log("Viewing login")},
                //         // { path: "/signup/", view: () => console.log("Viewing signup")},
                //     ];
                
                //     const potentialMatches = routes.map(route => {
                    //         return {
                        //             route: route,
                        //             isMatch: location.pathname === route.path
                        //         };
                        //     });
                        
                        //     let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);
                        
                        //     if (!match) {
                            //         match = {
                                //             route: routes[0],
                                //             isMatch: true
                                //         }
                                //     }
                                
                                //     const route = new match.route;
                                
                                //     document.querySelector("#app").innerHTML = await route.view.getHtml();
                                
                                //     console.log(match.route.view());
                                // };
                                
                                // window.addEventListener("popstate", router);
                                
                                // document.addEventListener("DOMContentLoaded", () => {
                                    //     document.body.addEventListener("click", e => {
                                        //         if (e.target.matches("[data-link]")) {
                                            //             e.preventDefault();
                                            //             navigateTo(e.target.href);
                                            //         };
                                            //     })
                                            //     router();
                                            // });
      
// import Home from "../views/home.js"

// const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

// const getParams = match => {
//     const values = match.result.slice(1);
//     const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

//     return Object.fromEntries(keys.map((key, i) => {
//         return [key, values[i]];
//     }));
// };

// const navigateTo = url => {
//     history.pushState(null, null, url);
//     router();
// };

// const router = async () => {
//     const routes = [
//         { path: "/", view: () => home},
//         { path: "/login/", view: () => home}
//         // { path: "/signup/", view: () => console.log("Viewing signup")},
//     ];

//     // Test each route for potential match
//     const potentialMatches = routes.map(route => {
//         return {
//             route: route,
//             result: location.pathname.match(pathToRegex(route.path))
//         };
//     });

//     let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);

//     if (!match) {
//         match = {
//             route: routes[0],
//             result: [location.pathname]
//         };
//     }

//     const view = new match.route.view(getParams(match));

//     document.querySelector("#app").innerHTML = await view.getHtml();
// };

// window.addEventListener("popstate", router);

// document.addEventListener("DOMContentLoaded", () => {
//     document.body.addEventListener("click", e => {
//         if (e.target.matches("[data-link]")) {
//             e.preventDefault();
//             navigateTo(e.target.href);
//         }
//     });

//     router();
// });


// Import the Home view class
import Home from "../views/home.js";
import Login from "../views/login.js";

// Define a function to convert path to regex
const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

// Function to extract parameters from a match
const getParams = match => {
    const values = match.result.slice(1);
    const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

    return Object.fromEntries(keys.map((key, i) => {
        return [key, values[i]];
    }));
};

// Function to navigate to a URL
const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

// Router function
const router = async () => {
    // Define routes
    console.log("Router function called");
    const routes = [
        { path: "/", view: Home },
        { path: "/login/", view: Login } // Assuming login also uses the Home view
        // { path: "/signup/", view: () => console.log("Viewing signup")},
    ];

    // Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            result: location.pathname.match(pathToRegex(route.path))
        };
    });

    // Find the first matching route
    let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);

    // If no match found, default to the first route
    if (!match) {
        match = {
            route: routes[0],
            result: [location.pathname]
        };
    }

    // Instantiate the view and render it
    const view = new match.route.view(getParams(match));
    document.querySelector("#app").innerHTML = await view.getHtml();
};

// Listen for popstate event and trigger router
window.addEventListener("popstate", router);

// Listen for DOMContentLoaded event and trigger router
document.addEventListener("DOMContentLoaded", () => {
    // Listen for click events on elements with data-link attribute
    document.body.addEventListener("click", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }
    });

    // Initial router call
    router();
});

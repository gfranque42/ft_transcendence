import abstractviews from "./abstractviews.js";
import {getCookie} from "../js/cookie.js";
import {navigateToInstead} from "../js/index.js";


// var DICT = {
//     "sms": false,
//     "email": false,
//     "app": false,
// };

function isEmptyOrWhitespace(str) {
    return !str || /^\s*$/.test(str);
}

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Profile");
    }

    async getHtml() 
    {
        const token = getCookie("token")
        
        if (token == null) {
            navigateToInstead("/login/");
            return ;
        }
        console.log("token Profile: " + token);
        
        const options = {
            method: 'GET',
            headers: {
                'http_x_fetch_request': true,
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        };
        
        const response = await fetch('https://localhost:8083/auth/profile', options);
        const tempContentHtml = await response.text();
        

        if (response.status != 200) {
            navigateToInstead("/");
            return ;
        }
        // Extract CSRF token from HTML form
        const parser = new DOMParser();
        const doc = parser.parseFromString(tempContentHtml, 'text/html');
        this.csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;      

        return tempContentHtml;
    }

    async profileUserPatch(token, username, avatar) {
        if (this.csrfToken === null) {
            throw new Error('CSRF token not available');
        }

        // const body = {};
        let formdata = new FormData();


        formdata.append('username', username.value);
        formdata.append('avatar', avatar.files[0]);
        formdata.append('token', await token);

        let response = await fetch('https://localhost:8083/auth/profile', {
            method: 'PATCH',
            body: formdata,
            headers: {
                // 'Content-Type': "application/x-www-form-urlencoded",
                'X-CSRFToken': this.csrfToken,
            },
        });
        const data = await response.json();

        return data;
    }

    async profileUserPost(token, email, sms, otp, app) {
        if (this.csrfToken === null) {
            throw new Error('CSRF token not available');
        }

        const body = {};
        // Always include the CSRF token and token
        body["csrfmiddlewaretoken"] = this.csrfToken;
        body["token"] = await token;
        
        
        // console.log("!", DICT, "!");
        
        // Conditionally add properties if they have values
        if (sms !== null && !isEmptyOrWhitespace(sms.value))
            body["phone_number"] = sms.value;
        if (email !== null && !isEmptyOrWhitespace(email.value))
            body["email"] = email.value;
        if (app.checked)
            body["app"] = app.value;
        if (otp && !isEmptyOrWhitespace(otp.value))
            body["otp"] = otp.value;
        // console.log("!", DICT, "!");
        let response = await fetch('https://localhost:8083/auth/verification-add', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
        });
        const data = await response.json();
        console.log(data);
        // console.log(DICT);

        // if (data.otp)
        // {
        //     DICT["email"] = false;
        //     DICT["app"] = false;
        //     DICT["sms"] = false;
        // }
        // console.log(DICT);
                
        return data;
    }


    // async VerificationNotVerified(token) {
    //     if (this.csrfToken === null) {
    //         throw new Error('CSRF token not available');
    //     }
    //     console.log("Deleting Verification");
    //     // Always include the CSRF token and token
    //     DICT["csrfmiddlewaretoken"] = this.csrfToken;
    //     DICT["token"] = await token;

    //     // Conditionally add properties if they have values
    //     console.log(DICT);
    //     let response = await fetch('https://localhost:8083/auth/verification-add', {
    //         method: 'DELETE',
    //         body: JSON.stringify(DICT),
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': this.csrfToken
    //         },
    //     });
    //     const data = await response.json();

    //     // DICT["email"] = false;
    //     // DICT["app"] = false;
    //     // DICT["sms"] = false;

    //     console.log(data);
    //     return data;
    // }

    async friendRequest(token, checkbox, fromUser) {
        // let formdata = new FormData();
        
        // formdata.append('token', await token);
        // formdata.append('from_user_id', fromUser);
        
        const body = {};

        // Always include the CSRF token and token
        body["token"] = await token;
        body["from_user_id"] = fromUser;

        let response;
        if (checkbox)
        {
            response = await fetch('https://localhost:8083/auth/send-friend-request', {
                method: 'PATCH',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
            });
        } else {
            response = await fetch('https://localhost:8083/auth/send-friend-request', {
                method: 'DELETE',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
            });
        }
        
        const data = await response.json();

        return data;
        
    }


    async sendFriendRequest(UserToken, to_user) {
        const token = await UserToken;
        
        const body = {};

        // Always include the CSRF token and token
        body["token"] = await token;
        body["to_user"] = to_user.value;

        const response = await fetch('https://localhost:8083/auth/send-friend-request', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
        });

        const data = await response.json();


        return data;
    }


    async deleteFriend(UserToken, friend) {
        const token = await UserToken;
        
        const body = {};

        // Always include the CSRF token and token
        body["friend_id"] = friend.value;
        body["token"] = await token;

        const response = await fetch('https://localhost:8083/auth/friends', {
            method: 'DELETE',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
                "Authorization": "Token " + token
            },
        });

        const data = await response.json();


        return data;
    }


    setTitle(title) {
        document.title = title;
    }
}
import abstractviews from "./abstractviews.js";

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

	async getUser()
	{
		const token = getCookie('token');
	
		const options = {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`
			}
		};
	
		const response = await fetch('https://localhost:8083/auth/test_token', options);
		const UserInformation = await response.json();
		console.log(UserInformation);
	
		return UserInformation;
	}

        const data = await response.json();
        // if (data.form.username)
        // console.log(data.token);
        return data;
    }

    setTitle(title) {
        document.title = title;
    }
}

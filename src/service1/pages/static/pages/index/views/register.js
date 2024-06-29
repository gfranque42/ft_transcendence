import abstractviews from "./abstractviews.js";

export default class extends abstractviews {
    constructor() 
    {
        super();
        this.setTitle("Register");
    }

	async getHtml() 
	{
		const response = await fetch('http://localhost:8082/auth/register'); // put the endpoint
		const tempContentHtml = await response.text();
		const tempContainer = document.createElement('div');
		tempContainer.innerHTML = tempContentHtml;
		// console.log(tempContainer);
		return tempContainer.innerHTML;
	}

    setTitle(title) {
        document.title = title;
    }
}
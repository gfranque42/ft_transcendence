export function generateRandomUrl() {
	const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	let str = '';
	for (let i = 0; i < 10; i++) {
		const randomIndex = Math.floor(Math.random() * characters.length);
		str += characters[randomIndex];
	}
	return str;
}

//create a waiting loop and get the elo from the user data
export function joinRoom()
{
	const roomUrl = generateRandomUrl();

	try
	{
		const tempContentHtml = document.body.innerHTML;
		console.log('tempContentHtml: ', tempContentHtml);
		// Extract CSRF token from HTML form
		const parser = new DOMParser();
		const doc = parser.parseFromString(tempContentHtml, 'text/html');
		const csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;
		console.log('csrfToken: ', csrfToken);

		// console.log('dns: ', dns);
		// const fetchurl = 'http://' + dns + ':8002/api_pong/postroom/';
		// console.log('fetchurl: ', fetchurl);
		const response = await fetch('/sudokubattle/api/sudoku/create/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrfToken,
			},
			body: JSON.stringify(roomData),
		});

		if (response.ok)
		{
			const responseData = await response.json();
			console.log('Room created: ', responseData);
		}
		else
		{
			console.error('Failed to create a room: ', response.statusText);
		}
	}
	catch (error)
	{
		console.error('Error: ', error);
		return ;
	}
	const link = document.createElement('a');
    link.href = '/sudoku/' + roomUrl + '/';
    link.setAttribute('data-link', '');
    document.body.appendChild(link);
    console.log(link);
    link.click();
    document.body.removeChild(link);
}

/*
game modes:
	-1 = no modes
	0 = easy
	1 = medium
	2 = hard
*/

let	gameMode = -1;

function Solo()
{
	let solo = document.querySelector('.Solo');
	let pvp = document.querySelector('.PvP');
	solo.style.backgroundColor = '#FFFBFC';
	solo.style.color = '#726DA8';
	pvp.style.backgroundColor = '';
	pvp.style.color = '';
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.display = 'block';
	medium.style.display = 'block';
	hard.style.display = 'block';
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = -1;
}

function PvP()
{
	let pvp = document.querySelector('.PvP');
	let solo = document.querySelector('.Solo');
	pvp.style.backgroundColor = '#FFFBFC';
	pvp.style.color = '#726DA8';
	solo.style.backgroundColor = '';
	solo.style.color = '';
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.display = 'block';
	medium.style.display = 'block';
	hard.style.display = 'block';
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = -1;
}

function Easy()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '4vh';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = 0;
}

function Medium()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '';
	medium.style.fontSize = '4vh';
	hard.style.fontSize = '';
	gameMode = 1;
}

function Hard()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '4vh';
	gameMode = 2;
}

function generateRandomUrl() {
	const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
	let str = '';
	for (let i = 0; i < 10; i++) {
		const randomIndex = Math.floor(Math.random() * characters.length);
		str += characters[randomIndex];
	}
	return str;
}

function getCookie(name)
{
	let cookieValue = null;
	if (document.cookie && document.cookie !== '')
	{
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++)
		{
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === `${name}=`)
			{
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

async	function getUser()
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

async	function Start()
{
	getUser();
	console.log('Start button clicked');
	if (gameMode == -1)
		return ;
	const roomUrl = generateRandomUrl();
	console.log('Room URL: ', roomUrl);
	const roomData = {
		url: roomUrl,
		difficulty: gameMode,
	};
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
	console.log("Start !");
	const link = document.createElement('a');
    link.href = '/sudokubattle/' + roomUrl + '/';
    link.setAttribute('data-link', '');
    document.body.appendChild(link);
    console.log(link);
    link.click();
    document.body.removeChild(link);
}

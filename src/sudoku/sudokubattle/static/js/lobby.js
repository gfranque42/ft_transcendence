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

function generateRandomUrl()
{
	let str = '';
	let i = 0;
	
	while (i < 10)
	{
		const n = Math.floor(Math.random() * 127);
		
		if (n > 47 && n < 91)
		{
			str += String.fromCharCode(n);
			i++;
		}
		else if (n > 96 && n < 123)
		{
			str += String.fromCharCode(n);
			i++;
		}
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

async	function Start()
{
	if (gameMode == -1)
		return ;
	const roomUrl = generateRandomUrl();
	const roomData = {
		url: roomUrl,
		difficulty: gameMode,
	};
	try
	{
		// console.log('dns: ', dns);
		// const fetchurl = 'http://' + dns + ':8002/api_pong/postroom/';
		// console.log('fetchurl: ', fetchurl);
		const response = await fetch('/sudokubattle/api/sudoku/create/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
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
		console.error('Error: ',error);
		return ;
	}
	console.log("Start !");
	window.location.pathname = '/sudokubattle/' + roomUrl + '/';
}

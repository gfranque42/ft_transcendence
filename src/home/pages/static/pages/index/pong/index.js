/*
game modes:
	-1 = no modes
	0 = pvp
	1 = pva easy
	2 = pva medium
	3 = pva hard
*/
import Pong from "../views/pong.js";

let	gameMode = -1;

function PvA()
{
	let pva = document.querySelector('.PvA');
	let pvp = document.querySelector('.PvP');
	pva.style.backgroundColor = '#FFFBFC';
	pva.style.color = '#53917E';
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
	let pva = document.querySelector('.PvA');
	pvp.style.backgroundColor = '#FFFBFC';
	pvp.style.color = '#53917E';
	pva.style.backgroundColor = '';
	pva.style.color = '';
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.display = '';
	medium.style.display = '';
	hard.style.display = '';
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = 0;
}

function Easy()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '4vh';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = 1;
}

function Medium()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '';
	medium.style.fontSize = '4vh';
	hard.style.fontSize = '';
	gameMode = 2;
}

function Hard()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '4vh';
	gameMode = 3;
}

function generateRandomUrl()
{
	let str = '';
    let i = 0;
	
    while (i < 10)
	{
		const n = Math.floor(Math.random() * 127);
		
		if (n > 47 && n < 58)
		{
			str += String.fromCharCode(n);
			i++;
		}
		else if (n > 64 && n < 91)
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
	console.log("cookie: ", cookieValue);
	return cookieValue;
}

export async	function Start(csrftoken, url)
{
	if (gameMode == -1)
		return ;
	let maxPlayers = 1;
	if (gameMode == 0)
		maxPlayers = 2;
	let roomUrl = generateRandomUrl();
	if (url != "blop")
		roomUrl = url;
	const roomData = {
		url: roomUrl,
		difficulty: gameMode,
		maxPlayers: maxPlayers,
	};
	try
	{
		getCookie('token');
		// console.log('dns: ', dns);
		const fetchurl = 'https://localhost:8083/api_pong/postroom/';
		// const fetchurl = 'http://' + dns + ':8002/api_pong/postroom/';
		console.log('fetchurl: ', fetchurl);
		const response = await fetch(fetchurl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
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
	// window.location.pathname = '/pong/' + roomUrl + '/';
	// const link = document.createElement('a');
	// link.href = '/pong/' + roomUrl + '/';
	// document.body.appendChild(link);
	// window.location.href = '/pong/' + roomUrl + '/';
	
	const link = document.createElement('a');
	link.href = '/pong/' + roomUrl + '/';
	link.setAttribute('data-link', '');
	document.body.appendChild(link);
	console.log(link);
	link.click();
	document.body.removeChild(link);
}

export function eventPong(view)
{
	document.addEventListener('click', function(event)
	{
		if (event.target.matches('.Start'))
		{
			view.PongLobbyCreation();
		}
		else if (event.target.matches('.PvP'))
		{
			PvP();
		}
		else if (event.target.matches('.PvA'))
		{
			PvA();
		}
		else if (event.target.matches('.Easy'))
		{
			Easy();
		}
		else if (event.target.matches('.Medium'))
		{
			Medium();
		}
		else if (event.target.matches('.Hard'))
		{
			Hard();
		}
	});
}
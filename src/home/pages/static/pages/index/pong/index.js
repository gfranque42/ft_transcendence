import {DNS} from "../js/dns.js";

/*
game modes:
	-1 = no modes
	0 = pvp
	1 = pva easy
	2 = pva medium
	3 = pva hard
*/
import Pong from "../views/pong.js";
import { navigateToInstead } from "../js/index.js";
let	gameMode = -1;

function PvA()
{
	let pva = document.querySelector('.PvA');
	let pvp = document.querySelector('.PvP');
	let localp = document.querySelector('.LocalP');
	let tournament = document.querySelector('.Tournament');
	pva.style.backgroundColor = '#FFFBFC';
	pva.style.color = '#53917E';
	pvp.style.backgroundColor = '';
	pvp.style.color = '';
	localp.style.backgroundColor = '';
	localp.style.color = '';
	tournament.style.backgroundColor = '';
	tournament.style.color = '';
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
	let localp = document.querySelector('.LocalP');
	let tournament = document.querySelector('.Tournament');
	pvp.style.backgroundColor = '#FFFBFC';
	pvp.style.color = '#53917E';
	pva.style.backgroundColor = '';
	pva.style.color = '';
	localp.style.backgroundColor = '';
	localp.style.color = '';
	tournament.style.backgroundColor = '';
	tournament.style.color = '';
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

function LocalP()
{
	let pvp = document.querySelector('.PvP');
	let pva = document.querySelector('.PvA');
	let localp = document.querySelector('.LocalP');
	let tournament = document.querySelector('.Tournament');
	localp.style.backgroundColor = '#FFFBFC';
	localp.style.color = '#53917E';
	tournament.style.backgroundColor = '';
	tournament.style.color = '';
	pvp.style.backgroundColor = '';
	pvp.style.color = '';
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
	gameMode = 4;
}

function Tournament()
{
	let pvp = document.querySelector('.PvP');
	let pva = document.querySelector('.PvA');
	let localp = document.querySelector('.LocalP');
	let tournament = document.querySelector('.Tournament');
	tournament.style.backgroundColor = '#FFFBFC';
	tournament.style.color = '#53917E';
	pvp.style.backgroundColor = '';
	pvp.style.color = '';
	pva.style.backgroundColor = '';
	pva.style.color = '';
	localp.style.backgroundColor = '';
	localp.style.color = '';
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.display = '';
	medium.style.display = '';
	hard.style.display = '';
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = 5;
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

async function checkRoom(options, gameMode)
{
	const response = await fetch('https://'+DNS+':8083/api_pong/getroom?request_by=Home', options);
	const rooms = await response.json();
	console.log('rooms:',rooms);
	for (let i = 0; i < rooms.length; i++)
	{
		console.log("i = ",i," rooms[i].maxPlayers - players.length = ",(rooms[i].maxPlayers - rooms[i].playerCount));
		console.log("i = ",i," rooms[i].maxPlayers = ",(rooms[i].maxPlayers));
		console.log("i = ",i," players.length = ",rooms[i].playerCount);
		if (gameMode == rooms[i].difficulty && (rooms[i].maxPlayers - rooms[i].playerCount) == 1)
		{
			console.log(rooms[i]);
			return (rooms[i].url);
		}
	}
	for (let i = 0; i < rooms.length; i++)
	{
		if (gameMode == rooms[i].difficulty && (rooms[i].maxPlayers - rooms[i].playerCount) == 2)
		{
			console.log(rooms[i]);
			return (rooms[i].url);
		}
	}
	return "None";
}

export async	function Start(csrftoken, Mode)
{
	checkConnection();
	if (Mode == -1)
		return ;
	let maxPlayers = 1;
	if (Mode == 0 || Mode == 5)
		maxPlayers = 2;
	if (Mode == 4)
		maxPlayers = 0;
	let roomExist = 0;
	let roomUrl = generateRandomUrl();
	try
	{
		const cookie = getCookie('token');

		const options = {
			method: 'GET', // HTTP method
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${cookie}`
			}
			};
		const str = await checkRoom(options, Mode);
		if ((Mode == 0 || Mode == 5) && str != "None")
		{
			roomExist = 1;
			roomUrl = str;
		}
	}
	catch (error)
	{
		console.error('Error: ',error);
		return ;
	}
	const roomData = {
		url: roomUrl,
		difficulty: Mode,
		maxPlayers: maxPlayers,
	};
	try
	{
		if (roomExist == 0)
		{
			getCookie('token');
			// console.log('dns: ', dns);
			const fetchurl = 'https://'+DNS+':8083/api_pong/postroom/?request_by=Home';
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
	}
	catch (error)
	{
		console.error('Error: ',error);
		return ;
	}
	console.log("Start !");
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
			view.PongLobbyCreation(gameMode);
		}
		else if (event.target.matches('.PvP'))
		{
			PvP();
		}
		else if (event.target.matches('.PvA'))
		{
			PvA();
		}
		else if (event.target.matches('.LocalP'))
		{
			LocalP();
		}
		else if (event.target.matches('.Tournament'))
		{
			Tournament();
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

export async function checkConnection()
{
	const cookie = getCookie('token');

	const options = {
		method: 'GET', // HTTP method
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Token ${cookie}`
		}

	};

	const response = await fetch('https://'+DNS+':8083/auth/test_token?request_by=Home', options);
	if (!response.ok)
	{
		navigateToInstead("/login/");
	}
}

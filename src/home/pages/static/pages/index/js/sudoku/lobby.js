import { getUser } from '../getUser.js';
import { navigateTo  } from '../index.js';


/*
game modes:
	-1 = no modes
	0 = easy
	1 = medium
	2 = hard
*/

let	gameMode = -1;
let multiplayer = false;

export async function changeUsername(view)
{
	const username = document.querySelector('.username');
}

export function Solo()
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
	multiplayer = false;
}

export function PvP()
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
	multiplayer = true;
}

export function Easy()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '4vh';
	medium.style.fontSize = '';
	hard.style.fontSize = '';
	gameMode = 0;
}

export function Medium()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '';
	medium.style.fontSize = '4vh';
	hard.style.fontSize = '';
	gameMode = 1;
}

export function Hard()
{
	let easy = document.querySelector('.Easy');
	let medium = document.querySelector('.Medium');
	let hard = document.querySelector('.Hard');
	easy.style.fontSize = '';
	medium.style.fontSize = '';
	hard.style.fontSize = '4vh';
	gameMode = 2;
}

export function getCookie(name)
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

export async function Start()
{
	const userInfo = await getUser();
	if (userInfo.expired) {
		navigateTo('/login/');
		return ;
	}

	if (gameMode == -1) {
		alert('Please select a game mode');
		return ;
	}

	const roomData = {
		difficulty: gameMode,
		user: userInfo.Username,
		id: userInfo.ID,
		multiplayer: multiplayer,
	};

	try
	{
		const tempContentHtml = document.body.innerHTML;
		const parser = new DOMParser();
		const doc = parser.parseFromString(tempContentHtml, 'text/html');
		const csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

		const response = await fetch('/sudokubattle/api/sudoku/create/?request_by=Home', {
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
			const roomUrl = responseData.roomUrl;
			navigateTo(`/sudoku/${roomUrl}/`);
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
	console.log("Start!");
}

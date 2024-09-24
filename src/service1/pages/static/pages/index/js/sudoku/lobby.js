/*
game modes:
	-1 = no modes
	0 = easy
	1 = medium
	2 = hard
*/

let	gameMode = -1;

export async function changeUsername(view)
{
	const username = document.querySelector('.username');

	user = await view.getUser();
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

// async	export function getUser()
// {
// 	const token = getCookie('token');

// 	const options = {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Token ${token}`
//         }
//     };

// 	const response = await fetch('https://localhost:8083/auth/test_token', options);
// 	const UserInformation = await response.json();
// 	console.log(UserInformation);

// 	return UserInformation;
// }

export async function Start(view)
{
	view.getUser();
	console.log('Start button clicked');
	if (gameMode == -1)
		return ;
	const roomData = {
		difficulty: gameMode,
	};

	console.log("Start !");
	const link = document.createElement('a');
    link.href = '/sudoku/waiting-room/';
    link.setAttribute('data-link', '');
    document.body.appendChild(link);
    console.log(link);
    link.click();
    document.body.removeChild(link);
	// Send a post request to go to the waiting room with the gamemode
}

import {setCookie, getCookie, eraseCookie} from "../cookie.js";

export async function sendGameResults(winner_id, loser_id, score_winner, score_loser) {
	const token = getCookie("token")

	console.log("hi this is stan");

	const options = {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Token ${token}`
		}
	};
	
	console.log("hi this is stan2");
	var response = await fetch('https://localhost:8083/auth/games', options);
	console.log(response);

	var data = await response.json();
	console.log(data);
	console.log("hi this is stan3");


	const body = {};

	if (response.status !== 200) {
		return data;
	}
	body["winner_id"] = winner_id;
	body["loser_id"] = loser_id;
	body["score_winner"] = score_winner;
	body["score_loser"] = score_loser;
	body["game_type"] = 'sudoku';
	console.log("hi this is stan3");


	var response = await fetch('https://localhost:8083/auth/games', {
		method: 'POST',
		body: JSON.stringify(body),
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': data.csrfToken
		},
	});
	console.log("hi this is stan3");


	data = await response.json();
	console.log(data);
	console.log("hi this is stan3");

	return data;
}

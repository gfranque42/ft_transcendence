
import {setCookie, getCookie, eraseCookie} from "../js/cookie.js";

export async function getUser()
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


import {setCookie, getCookie, eraseCookie} from "../js/cookie.js";

export async function getUser()
{
	const token = getCookie('token');
	if (!token)
	{
		return null;
	}
	const options = {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Token ${token}`
		}
	};

	const response = await fetch('https://localhost:8083/auth/test_token?request_by=Home', options);
	const UserInformation = await response.json();

	return UserInformation;
}

import {DNS} from "./dns.js";

async function updateUserStatus(UserToken) {
	const token = await UserToken;

	
	// Always include the CSRF token and token
	
	const response = await fetch('https://'+DNS+':8083/auth/user-status?request_by=Home', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			"Authorization": "Token " + token
		},
	});

	const data = await response.json();


	return data;
}
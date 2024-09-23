async function updateUserStatus(UserToken) {
	const token = await UserToken;

	
	// Always include the CSRF token and token
	
	const response = await fetch('https://localhost:8083/auth/user-status', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			"Authorization": "Token " + token
		},
	});

	const data = await response.json();

	console.log(data);

	return data;
}
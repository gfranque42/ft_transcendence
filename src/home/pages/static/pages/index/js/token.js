
export async function getRenewedToken(token) {

	const options = {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Token ${token}`
		}
	};

	const response = await fetch('https://localhost:8083/auth/get_token?request_by=Home', options);
	const newToken = await response.json();

	if (!newToken)
		return null;
	return newToken.token
}
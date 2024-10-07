
export async function getRenewedToken(token) {

	const options = {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Requested-by': 'Home',
			'Authorization': `Token ${token}`
		}
	};

	const response = await fetch('https://localhost:8083/auth/get_token', options);
	const newToken = await response.json();

	if (!newToken)
		return null;
	return newToken.token
}
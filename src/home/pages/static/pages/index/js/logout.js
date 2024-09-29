
export async function logout(userToken) {
	const token = await userToken;
	
	if (!token)
		return null;

	let response = await fetch('https://localhost:8083/auth/logout', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
            'Authorization': `Token ${await token}`
		},
	});

	console.log("logout");

	const data = await response.json();
	return null;
}
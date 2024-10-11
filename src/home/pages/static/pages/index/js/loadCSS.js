export function loadCSS(url) {
	const link = document.createElement('link');
	link.rel = 'stylesheet';
	link.href = url;
	
	// Append the link element to the head
	console.log("CSS Loading: " + url);
	document.head.appendChild(link);

	// Optionally, you can add a listener for when the CSS is loaded
	link.onload = () => {
		console.log('CSS loaded successfully:', url);
	};

	link.onerror = () => {
		console.error('Error loading CSS:', url);
	};
}
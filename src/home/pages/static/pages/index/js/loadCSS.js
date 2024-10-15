export function loadCSS(url) {
	const link = document.createElement('link');
	link.rel = 'stylesheet';
	link.href = url;
	
	document.head.appendChild(link);

	link.onload = () => {
		console.log('CSS loaded successfully:', url);
	};

	link.onerror = () => {
		console.error('Error loading CSS:', url);
	};
}

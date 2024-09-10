
export function setCookie(name, value, minutes) {
    let expires = "";
    if (minutes) {
        const date = new Date();
        date.setTime(date.getTime() + (minutes * 60 * 1000)); // Convert minutes to milliseconds
        expires = "; expires=" + date.toUTCString();
    }
    // document.cookie = name + "=" + (value || "") + expires + "; path=/cookie/; SameSite=None; Secure";
    console.log(document.cookie);

    document.cookie = name + "=" + (value || "") + "; expires=" + expires + "; path=/; SameSite=None; Secure";

    console.log(document.cookie);
    console.log(name);

}

export function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

export function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999; path=/';
}

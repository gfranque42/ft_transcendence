import { DNS } from "../js/dns.js";

/*
game modes:
	-1 = no modes
	0 = pvp
	1 = pva easy
	2 = pva medium
	3 = pva hard
*/
import Pong from "../views/pong.js";
import { navigateToInstead } from "../js/index.js";
let gameMode = -1;

function PvA() {
  let pva = document.querySelector(".PvA");
  let pvp = document.querySelector(".PvP");
  let localp = document.querySelector(".LocalP");
  let tournament = document.querySelector(".Tournament");
  pva.style.backgroundColor = "#FFFBFC";
  pva.style.color = "#53917E";
  pvp.style.backgroundColor = "";
  pvp.style.color = "";
  localp.style.backgroundColor = "";
  localp.style.color = "";
  tournament.style.backgroundColor = "";
  tournament.style.color = "";
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.display = "block";
  medium.style.display = "block";
  hard.style.display = "block";
  easy.style.fontSize = "";
  medium.style.fontSize = "";
  hard.style.fontSize = "";
  gameMode = -1;
}

function PvP() {
  let pvp = document.querySelector(".PvP");
  let pva = document.querySelector(".PvA");
  let localp = document.querySelector(".LocalP");
  let tournament = document.querySelector(".Tournament");
  pvp.style.backgroundColor = "#FFFBFC";
  pvp.style.color = "#53917E";
  pva.style.backgroundColor = "";
  pva.style.color = "";
  localp.style.backgroundColor = "";
  localp.style.color = "";
  tournament.style.backgroundColor = "";
  tournament.style.color = "";
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.display = "";
  medium.style.display = "";
  hard.style.display = "";
  easy.style.fontSize = "";
  medium.style.fontSize = "";
  hard.style.fontSize = "";
  gameMode = 0;
}

function LocalP() {
  let pvp = document.querySelector(".PvP");
  let pva = document.querySelector(".PvA");
  let localp = document.querySelector(".LocalP");
  let tournament = document.querySelector(".Tournament");
  localp.style.backgroundColor = "#FFFBFC";
  localp.style.color = "#53917E";
  tournament.style.backgroundColor = "";
  tournament.style.color = "";
  pvp.style.backgroundColor = "";
  pvp.style.color = "";
  pva.style.backgroundColor = "";
  pva.style.color = "";
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.display = "";
  medium.style.display = "";
  hard.style.display = "";
  easy.style.fontSize = "";
  medium.style.fontSize = "";
  hard.style.fontSize = "";
  gameMode = 4;
}

function Tournament() {
  let pvp = document.querySelector(".PvP");
  let pva = document.querySelector(".PvA");
  let localp = document.querySelector(".LocalP");
  let tournament = document.querySelector(".Tournament");
  tournament.style.backgroundColor = "#FFFBFC";
  tournament.style.color = "#53917E";
  pvp.style.backgroundColor = "";
  pvp.style.color = "";
  pva.style.backgroundColor = "";
  pva.style.color = "";
  localp.style.backgroundColor = "";
  localp.style.color = "";
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.display = "";
  medium.style.display = "";
  hard.style.display = "";
  easy.style.fontSize = "";
  medium.style.fontSize = "";
  hard.style.fontSize = "";
  gameMode = 5;
}

function Easy() {
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.fontSize = "4vh";
  medium.style.fontSize = "";
  hard.style.fontSize = "";
  gameMode = 1;
}

function Medium() {
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.fontSize = "";
  medium.style.fontSize = "4vh";
  hard.style.fontSize = "";
  gameMode = 2;
}

function Hard() {
  let easy = document.querySelector(".Easy");
  let medium = document.querySelector(".Medium");
  let hard = document.querySelector(".Hard");
  easy.style.fontSize = "";
  medium.style.fontSize = "";
  hard.style.fontSize = "4vh";
  gameMode = 3;
}

function generateRandomUrl() {
  let str = "";
  let i = 0;

  while (i < 10) {
    const n = Math.floor(Math.random() * 127);

    if (n > 47 && n < 58) {
      str += String.fromCharCode(n);
      i++;
    } else if (n > 64 && n < 91) {
      str += String.fromCharCode(n);
      i++;
    } else if (n > 96 && n < 123) {
      str += String.fromCharCode(n);
      i++;
    }
  }
  return str;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function checkRoom(options, gameMode) {
  if (gameMode != 0) return "None";
  const response = await fetch(
    "https://" + DNS + ":8083/api_pong/getroom?request_by=Home",
    options
  );
  const rooms = await response.json();
  let room;
  for (let i = 0; i < rooms.length; i++) {
    if (
      gameMode == rooms[i].difficulty &&
      rooms[i].maxPlayers - rooms[i].playerCount == 1
    )
      return rooms[i].url;
  }
  for (let i = 0; i < rooms.length; i++) {
    if (
      gameMode == rooms[i].difficulty &&
      rooms[i].maxPlayers - rooms[i].playerCount == 2
    )
      return rooms[i].url;
  }
  return "None";
}

export async function Start(csrftoken, url) {
  checkConnection();
  const result = document.getElementById("url");
  const tournamentUrl = result.textContent;
  if (gameMode == -1) return;
  let maxPlayers = 1;
  if (gameMode == 0) maxPlayers = 2;
  if (gameMode == 4) maxPlayers = 0;
  let roomExist = 0;
  let roomUrl = generateRandomUrl();
  if (gameMode == 5) roomUrl = tournamentUrl;
  try {
    const cookie = getCookie("token");

    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${cookie}`,
      },
    };
    const str = await checkRoom(options, gameMode);
    if (gameMode == 0 && str != "None") {
      roomExist = 1;
      roomUrl = str;
    }
  } catch (error) {
    console.error("Error: ", error);
    return;
  }
  const roomData = {
    url: roomUrl,
    difficulty: gameMode,
    maxPlayers: maxPlayers,
  };
  if (gameMode != 5) {
    try {
      if (roomExist == 0) {
        getCookie("token");
        const fetchurl =
          "https://" + DNS + ":8083/api_pong/postroom/?request_by=Home";
        const response = await fetch(fetchurl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify(roomData),
        });
        if (response.ok) {
          const responseData = await response.json();
        } else {
          console.error("Failed to create a room: ", response.statusText);
        }
      }
    } catch (error) {
      console.error("Error: ", error);
      return;
    }
  }
  const link = document.createElement("a");
  link.href = "/pong/" + roomUrl + "/";
  link.setAttribute("data-link", "");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export function eventPong(view) {
  document.addEventListener("click", function (event) {
    if (event.target.matches(".Start")) {
      view.PongLobbyCreation();
    } else if (event.target.matches(".PvP")) {
      PvP();
    } else if (event.target.matches(".PvA")) {
      PvA();
    } else if (event.target.matches(".LocalP")) {
      LocalP();
    } else if (event.target.matches(".Tournament")) {
      Tournament();
    } else if (event.target.matches(".Easy")) {
      Easy();
    } else if (event.target.matches(".Medium")) {
      Medium();
    } else if (event.target.matches(".Hard")) {
      Hard();
    }
  });
}

export async function checkConnection() {
  const cookie = getCookie("token");

  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${cookie}`,
    },
  };

  const response = await fetch(
    "https://" + DNS + ":8083/auth/test_token?request_by=Home",
    options
  );
  if (!response.ok) {
    navigateToInstead("/login/");
  }
}

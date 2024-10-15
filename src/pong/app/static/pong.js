var socketProtocol = "ws://";

if (window.location.protocol === "https:") {
  socketProtocol = "wss://";
}

const roomSocket = new WebSocket(
  socketProtocol + window.location.host + "/ws" + window.location.pathname
);

function vec2(x, y) {
  return { x: x, y: y };
}

function paddle(pos, size) {
  this.pos = pos;
  this.size = size;

  this.update = function (pos, size) {
    this.pos = pos;
    this.size = size;
  };
}

function ball(pos, size) {
  this.pos = pos;
  this.size = size;

  this.update = function (pos, size) {
    this.pos = pos;
    this.size = size;
  };
}

function game(paddle1, paddle2, ball, player1, player2) {
  this.paddle1 = paddle1;
  this.paddle2 = paddle2;
  this.ball = ball;
  this.player1 = player1;
  this.player2 = player2;

  this.update = function (paddle1, paddle2, ball) {
    this.paddle1.update(paddle1.pos, paddle1.size);
    this.paddle2.update(paddle2.pos, paddle2.size);
    this.ball.update(ball.pos, ball.size);
  };
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

function waitForSocketConnection() {
  setTimeout(function () {
    if (roomSocket.readyState === 1) testToken();
    else waitForSocketConnection(roomSocket);
  }, 5);
}

async function testToken() {
  cookie = getCookie("token");

  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${cookie}`,
    },
  };

  const url = window.location.href;
  const finalurl = url.replace(window.location.pathname, "");
  const fetchurl = finalurl + "/auth/test_token/";

  const response = await fetch(fetchurl, options);
  const UserInformation = await response.json();

  roomSocket.send(
    JSON.stringify({
      type: "username",
      username: UserInformation.Username,
    })
  );
}

waitForSocketConnection();

let myGame = game(
  paddle(vec2(1, 1), vec2(1, 1)),
  paddle(vec2(1, 1), vec2(1, 1)),
  ball(vec2(1, 1), vec2(1, 1))
);

roomSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  if (data.type === "username") {
    console.log("username from serveur: ", data.username);
  }
};

roomSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};

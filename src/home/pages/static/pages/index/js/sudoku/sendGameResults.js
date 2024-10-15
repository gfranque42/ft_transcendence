import { setCookie, getCookie, eraseCookie } from "../cookie.js";
import { DNS } from "../dns.js";

export async function sendGameResults(
  winner_id,
  loser_id,
  score_winner,
  score_loser
) {
  const token = getCookie("token");

  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  };

  var response = await fetch(
    "https://" + DNS + ":8083/auth/games?request_by=Home",
    options
  );
  var data = await response.json();

  const body = {};

  if (response.status !== 200) {
    return data;
  }
  body["winner_id"] = winner_id;
  body["loser_id"] = loser_id;
  body["score_winner"] = score_winner;
  body["score_loser"] = score_loser;
  body["game_type"] = "sudoku";

  var response = await fetch(
    "https://" + DNS + ":8083/auth/games?request_by=Home",
    {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": data.csrfToken,
      },
    }
  );

  data = await response.json();
  return data;
}

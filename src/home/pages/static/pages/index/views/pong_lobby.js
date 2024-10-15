import abstractviews from "./abstractviews.js";
import { DNS } from "../js/dns.js";

export let csrfToken = null;

export default class extends abstractviews {
  constructor() {
    super();
    this.setTitle("PongLobby");
  }

  async getHtml() {
    const url = location.pathname;
    const bob = url.replace("/pong/", "");
    const room_name = bob.replace("/", "");
    const response = await fetch(
      "https://" +
        DNS +
        ":8083/api_pong/getlobby/" +
        room_name +
        "?request_by=Home"
    );
    const tempContentHtml = await response.text();

    const parser = new DOMParser();
    const doc = parser.parseFromString(tempContentHtml, "text/html");
    csrfToken = doc.querySelector('[name="csrfmiddlewaretoken"]').value;

    return tempContentHtml;
  }

  setTitle(title) {
    document.title = title;
  }
}

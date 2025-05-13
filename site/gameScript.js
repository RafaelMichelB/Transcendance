
adress = "localhost"

canvas = document.getElementById("gameCanvas")
const ctx = canvas.getContext("2d");
ctx.font = "20px Arial";
ctx.fillStyle = "blue";

function handleGame2Players(key, playerID, isAiGame) {
    url_sse = `http://${adress}:8000/events?apikey=${key}&idplayer=${playerID}&ai=${isAiGame}`;
    url_post = `http://${adress}:8000/send-message`;
    started = false;

    
    const SSEStream = new EventSource(url_sse);
    SSEStream.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            console.log(data);
        } catch (error) {
            console.log("ParsingError: ", error)
        }
    }

    document.addEventListener('keydown', function(event) {
        switch(event.key) {
            case "p" :
                if (playerID == 1 && started == false) {
                    fetch(adressDjangoGame, {
                        method: 'POST',
                        headers: {
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"apiKey": key, "message": '{"action": "start"}'})
                      }); break;
                }
            case "q" : fetch(`http://${adress}:8000/forfait-game?apikey=${key}&idplayer=${playerID}`); break;
            case "ArrowUp" : 
                if (playerID == 1) { 
                    fetch(adressDjangoGame, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"apiKey": val, "message": '{"action": "move", "player1": "up"}'})
                  });
                }
                else {
                    fetch(adressDjangoGame, {
                        method: 'POST',
                        headers: {
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"apiKey": val, "message": '{"action": "move", "player2": "up"}'})
                      });
                } ;
                break;
            case "ArrowDown" :
                if (playerID == 1) { 
                    fetch(adressDjangoGame, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"apiKey": val, "message": '{"action": "move", "player1": "up"}'})
                  });
                }
                else {
                    fetch(adressDjangoGame, {
                        method: 'POST',
                        headers: {
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"apiKey": val, "message": '{"action": "move", "player2": "up"}'})
                      });
                } ;
                break;
        }
    })

}

function isGamePlayable(apikey) {
    fetch(`http://${adress}:8000/is-game-playable?apikey=${apikey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"apiKey": apikey})
        .then(response => {
            if (!response.ok) throw new Error("HTTP Error: " + response.status);
            return response.json();
          })
          .then(data => {
            console.log("Données reçues SetKey:", data["playable"]);
            return data["playable"]
          })
          .catch(error => {
            console.error("Erreur de requête :", error);
          })
      });

}

function setApiKeyWeb(apikey) {
    fetch(`http://${adress}:8000/set-api-key`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"apiKey": apikey})
        .then(response => {
            if (!response.ok) throw new Error("HTTP Error: " + response.status);
            return response.json();
          })
          .then(data => {
            console.log("Données reçues SetKey:", data["playable"]);
            return data["playable"]
          })
          .catch(error => {
            console.error("Erreur de requête :", error);
          })
      });

}
function sendGameCreation() {
    fetch(`http://${adress}:8000/get-api-key`)
      .then(response => {
        if (!response.ok) throw new Error("HTTP Error: " + response.status);
        return response.json();
      })
      .then(data => {
        console.log("Données reçues :", data);
        ctx.fillText("Game State : ", 50, 50)
        ctx.fillText(`Room ID to give ${data}!`, 150, 150);
      })
      .catch(error => {
        console.error("Erreur de requête :", error);
      });
    let isGamePlayable = setApiKeyWeb(data)

}

// fetch(adressDjangoGame, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({"apiKey": key, "message": '{"action": "start"}'})
//   })
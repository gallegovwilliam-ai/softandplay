    var socket = new WebSocket(webSocketEndpoint); // Creating a new Web Socket Connection
    // Socket On receive message Functionality
    socket.onmessage = function(e){
        console.log('message', e);
          data = JSON.parse(e.data);
          if(data.reload == 'SI'){location.reload();return false;};
            if(data.ganador == 'termino'){
                document.getElementById('ganadores-items').innerHTML = "<img src='/static/img/luego.jpg' width='50%' style='border-radius:30px;margin-top:100px;'>";
                document.getElementById('content-ganador').style.display = 'block';
                return false;
            }
			if(data.ganador != 'none'){
				document.getElementById('ganadores-items').innerHTML = data.ganador;
                document.getElementById('content-ganador').style.display = 'block';
			}
			ultimas5 = data.ultimas5;
			numeroE = data.balota;
            if(document.getElementById("bell"+data.balota)){
                document.getElementById("bell"+data.balota).style.display ='none';
                document.getElementById("bell").play();
            }
			document.getElementById('balotasJugadas').innerHTML = data.balotasJugadas;
			myAudio.src = "/static/audio/" + data.balota + ".mp3";
			myAudio.load();
	       	$("#balotaE").attr("src", '/static/cards-masters/tapa.png');


    };
    // Socket Connet Functionality
    socket.onopen = function(e){
       console.log('open',e);
    };
    // Socket Error Functionality
    socket.onerror = function(e){
        console.log('error',e);
    };
    // Socket close Functionality
    socket.onclose = function(e){
        console.log('closed',e);
    };
  //FIN WEBSOCKET


    function reload(){
        data = {'reload':'SI'};
    var msg = {
    type: "notify",
    text: JSON.stringify(data),
    };
    // Send the msg object as a JSON-formatted string.
    socket.send(JSON.stringify(msg));
    }
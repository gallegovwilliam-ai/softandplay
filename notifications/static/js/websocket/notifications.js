    var socket = new WebSocket(webSocketEndpoint); // Creating a new Web Socket Connection
    // Socket On receive message Functionality
    socket.onmessage = function(e){
        console.log('message', e);
          a = JSON.parse(e.data);
          n1 = parseInt($('#count_message').text()) + parseInt(1);
         
          if (a.type=='app'){
            $('#count_notify').text(n1);
            $('#message_notifications').text('Tienes ' + $('#count_notify').text() + ' nuevas notificaciones');

            $("#new_notify").prepend("<i style='box-sizing: border-box;'><a style='padding: 15px 10px !important;width: 100%;display: inline-block;border-bottom: 1px solid #EBEBEB !important;font-size: 12px;list-style: none;' href='" + a.url +"'><span class='label label-info'><i class='fa fa-bolt'></i></span>" + a.message + "<span class='small italic'> " + a.timeago + " </span></a></i>");
                  $.notify({
                    // options
                      titlte: a.tittle,
                      url:a.url,          
                      message: a.message
                  },{
                    // settings
                    type: 'danger',
                    placement: {
                      from: "bottom",
                      align: "right"
                    },
                    delay: 120000,
                  });
          }
          if (a.type=='message'){
            var URLactual = window.location.toString();
            if (URLactual.indexOf("messages") > -1){
              if(a.username_emiter==userActive){
                $('.infinite-container').prepend("<div class='group-rom infinite-item'><div class='first-part odd'><img width='30px' height:'30px' style='border-radius:35%''  src='" + a.img + "'>&nbsp;&nbsp;" + a.user_emiter + "</div><div class='second-part'>" + a.message + "</div><div class='third-part'>" + a.timeago + "</div></div>");
              }
            }else{
              $('#count_message').text(n1);
              $('#message_messages').text('Tienes ' + $('#count_message').text() + ' nuevos mensajes');
              $("#new_message").prepend("<li><a href='" +  a.url + "'><span class='photo'><img alt='avatar' src='" + a.img + "'></span><span class='subject'><span class='from'>" + a.user_emiter + "</span><span class='time'>" + a.timeago + "</span></span><span class='message'>" + a.message + "</span></a></li>");
                  $.notify({
                    // options
                      titlte: a.tittle,
                      url:a.url,          
                      message: a.message
                  },{
                    // settings
                    type: 'danger',
                    placement: {
                      from: "bottom",
                      align: "right"
                    },
                    delay: 120000,
                  });
            }
          }
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
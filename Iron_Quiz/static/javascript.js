"use strict";

document.addEventListener("DOMContentLoaded", function (event) {
  let socket = io.connect(document.domain + ':' + location.port);

  socket.on('connect', function () {
    console.log('connected!');
    socket.emit('socketIsConnected')

    if (document.getElementsByTagName('input').length) {
      for (let input of document.getElementsByTagName('input')) {
        if (input["type"] === "submit") {
          input.addEventListener('mouseup', function (e) {
            socket.emit('submittingForm', { data: "some data" });

            console.log("yeeee");
          })
        }
      }
    }
  })

  socket.on('reload', function (booker) {
    let logged_user = document.getElementById("username")["innerText"]
    console.log("logged user" + logged_user);
    console.log("booker" + booker);
    if(logged_user === booker){
      console.log('reloading...');
      location.reload();
    }

  })
})
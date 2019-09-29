"use strict";

document.addEventListener("DOMContentLoaded", function (event) {
  let socket = io.connect(document.domain + ':' + location.port);

  socket.on('connect', function () {
    console.log('connected!');
    socket.emit('socketIsConnected')

    // if (document.getElementsByTagName('input').length) {
    //   for (let input of document.getElementsByTagName('input')) {
    //     if (input["type"] === "submit" && input["id"] === "submit_new_question") {
    //       input.addEventListener('mouseup', function (e) {
    //         socket.emit('reloadAllClients');

    //         console.log("yeeee");
    //       })
    //     }
    //   }
    // }
  })

  socket.on('reloadClient', function () {
    console.log('reloading this client...');

    window.location = window.location;
    // location.reload();

  })

  socket.on('reload', function () {
    console.log('reloading...');

    location.reload();

  })
})
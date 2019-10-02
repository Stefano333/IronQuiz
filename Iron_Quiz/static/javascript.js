"use strict";

document.addEventListener("DOMContentLoaded", function (event) {
  let socket = io.connect(document.domain + ':' + location.port);
  // manager = new socket.Manager('/socket.io', )

  socket.on('connect', function () {
    console.log('connected!');
    socket.emit('socketIsConnected')
  })

  socket.on('reloadClient', function () {
    console.log('reloading this client...');

    window.location = window.location;
    // location.reload();

  })

  socket.on('reload', function () {
    console.log('reloading...');

    location.reload();

    socket.onerror = function (error) {
      console.error('There was an un-identified Web Socket error');
    };
  })
})
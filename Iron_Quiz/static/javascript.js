"use strict";

document.addEventListener("DOMContentLoaded", function(event) { 
    let socket = io.connect('http://' + document.domain + ':' + location.port);
      socket.on( 'connect', function() {
        socket.emit( 'my event', {
          data: 'User Connected'
        } )
        let allowAnswer = document.getElementById('allow_answer').onsubmit = function( e ) {
          e.preventDefault()

          socket.emit( 'my event', {
            data : "some data"
          } )
        }
      } )
      socket.on( 'my response', function( msg ) {
        console.log( msg )
        }
      )
  });
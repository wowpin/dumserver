var net  = require( 'net' ),
      _  = require( 'underscore' ),
 config  = require( '../lib/config' ),
 logger  = require( '../lib/logger' );

var connected = {
  count: 0,
  games: {}
};

var whenConnected = function(address) {
  connected.count++;
  var key = address.host + ':' + address.port;
  key = key.toLowerCase();
  if (connected.games[key]) {
    connected.games[key]++;
  } else {
    connected.games[key] = 1;
  }
};
exports = module.exports;

exports.connected = function() {
  return {
    count: connected.count,
    games: _.sortBy( _.map( connected.games, function ( count, game ) { return { address: game, count: count }; } ), 'count' ).reverse()
  };
};

// browser connecting via websocket
exports.connection = function ( socket ) {

  //console.log( socket.handshake.query );

  var gameHost = config.moo.host;
  var gamePort = config.moo.port;
  if (socket.handshake['query'] && socket.handshake.query['host']) {
    gameHost = socket.handshake.query.host;
  }
  if (socket.handshake['query'] && socket.handshake.query['port']) {
    gamePort = socket.handshake.query.port;
  }

  // open a network connection to the moo
  socket.set( 'is-active', true );
  socket.set( 'game-address', { host: gameHost, port: gamePort } );

  var moo = net.connect( { 'port' : gamePort, 'host' : gameHost }, function(err) {
    // tell the other end of the connection that it connected successfully
    if (err) {
      logger.error( err );
      socket.set( 'is-active', false );
    } else {
      socket.get( 'game-address', function( err, address ) {
        whenConnected(address);
        socket.set( 'is-active', true );
        socket.emit( 'connected', ( new Date() ).toString() );
      });
    }
  });
  
  /*moo.on( 'connect', function( data ) {
    socket.get( 'game-address', function( err, address ) {
      whenConnected(address);
      socket.set( 'is-active', true );
      socket.emit( 'connected', ( new Date() ).toString() );
    });
  });*/
  
  // ** when receiving data from the moo
  moo.on( 'data', function( data ) {
    try {
      data = data.toString();
      if ( ( marker = data.indexOf( '#$# dome-client-user' ) ) != -1 ) {
        var end = data.indexOf( "\r\n", marker );
        // server wants to know the current remote address
        moo.write( "@dome-client-user " + socket.handshake.address.address + "\r\n", "utf8" );
      } else {
        socket.get( 'is-active', function( err, active ) {
            if ( active ) {
                socket.emit( 'data', data );
            }
        });
      }
    } catch (e) {
      logger.error('exception caught when receiving data from the moo', e);
    }
  });
  
  moo.on( 'end', function( ) {
    logger.debug('moo connect sent end');
    socket.get( 'is-active', function( err, active ) {
      if ( active ) {
        logger.debug('socket is active, sending disconnect and marking inactive');
        socket.set( 'is-active', false );
        socket.emit( 'disconnect' );
      } else {
        logger.debug('socket is no longer active');
      }
    });
  });
  
  moo.on( 'error', function(e) {
    logger.error( 'moo error event occurred' );
    logger.error( e );
      socket.get( 'is-active', function( err, active ) {
        if ( active ) {
          socket.emit( 'error', e );
        }
      });
  });
  
  socket.on( 'error', function(e) {
    logger.error( 'socket error event occurred' );
    logger.error( e );
    // can't send this to the user 
  });
  
  socket.on( 'disconnect', function( data ) {
    socket.set( 'is-active', false );
    logger.debug( 'disconnected from client with data:' );
    logger.debug( data );
    moo.write( '@quit' + "\r\n", "utf8", function() {
      moo.end();
    });
  });
  
  // ** when receiving input from the websocket connected browser
  socket.on( 'input', function( command, inputCallback ) {
    if ( command == null ) {
      // event received, but null or empty string
      inputCallback( new Error( 'no input' ) );
    } else {
      // write the command to the moo and finish with a line break
      try {
        moo.write( command + "\r\n", "utf8", function() {
          // we emit a status event back to the browser to confirm we've done our job
          socket.emit( 'status', 'sent ' + command.length + ' characters' );
          if ( command == '@quit' ) {
            moo.end();
            socket.set( 'is-active', false );
            socket.emit( 'disconnect' );
          }
        });
        if (inputCallback) inputCallback( { 'status' : 'command sent from ' + config.node.poweredBy + ' to moo at ' + (new Date()).toString() } );
      } catch ( exception ) {
        logger.error( 'exception while writing to moo' );
        logger.error( exception );
        socket.get( 'is-active', function( err, active ) {
          if ( active ) {
            socket.emit( 'error', exception ); 
          }
        });
      }
    }
  });
};
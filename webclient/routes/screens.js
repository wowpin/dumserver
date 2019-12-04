var logger = require( '../lib/logger' ),
    config = require( '../lib/config' ),
    fs     = require( 'fs' );

var exports = module.exports;
exports.connect = function( req, res ) {
  try {
    res.render( 'connect-as', { 
      'connectAnywhere': config.node.connectAnywhere, 
      'mooHostname': config.moo.host,
      'mooPort': config.moo.port,
      'meta' : {
       'title' : 'Connect',
       'description' : 'Connect to DUM using state of art Dome Client',
       'keywords' : 'moo-client, dome-client.js, mud client, telnet client, modern gaming client, text-based game, websocket-telnet'
      }
    });
  } catch( e ) {
    logger.debug('exception caught:');
    logger.debug(e);
  }
};

exports.options = function( req, res ) {
  res.render( 'client-options', {
    'meta' : {
      'title' : 'Options',
      'description': 'Configure your preferred options when using our state of the art Game Client.',
      'keywords': 'moo-client, mud-client,  dome-client.js, client options, configure preferences, command hints'
    }
  });
};

exports.client = function( req, res ) {
  res.render( 'client', {
    'meta' : {
      'title' : '' + 'Game Client',
      'description' : 'Someone playing ' + config.node.poweredBy + ' via its web-based game Client',
      'keywords' : 'moo-client, dome-client.js, telnet client, modern gaming client, text-based game, websocket-telnet'
    }
  });
};

exports.editor = function( req, res ) {
  var template = editorType = req.params.type;
  if ( editorType != "verb") {
    // only verb gets special support right now
    template = "basic";
  }
  res.render( 'editors/' + template, {
    editor : {
      'readonly' : req.params.type == "basic-readonly" ? true : false
    },
    'meta' : {
      'title' : 'Untitled Local Editor ',
      'description' : 'Local editor window for the dome-client.js client.',
      'keywords' : 'dome-client.js editor'      
    }
  });
}

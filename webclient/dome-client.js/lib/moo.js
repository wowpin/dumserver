/*
 * moo - functions for communicating directly with the moo
 * 
 */
var fs     = require( 'fs' ),
    net    = require( 'net' ),
    _      = require( 'underscore' ),
		config = require( './config' ),
		logger = require( './logger' ),
		reload = require( './reload' );

var

var DomeClient = function() {
  this.maxBuffer = 2500; // lines
  this.bufferPadding = 500; // lines
  this.buffer = [];
  this.connection = null;
  this.connect = function( host, port, next ) {
    this.connection = con = net.connect( host, port, function(data) {
      con.write( '#!# helo from dome-client.js' + "\r\n" );
    });
    this.connection.on( 'data', function( data ) {
      data = data.toString();
      var lines = data.split( /\r\n/ );
      for( var i = 0; i < lines.length; i++ ) {
        this.buffer[ this.buffer.length ] = lines[ i ];
      }
      if ( this.buffer.length > this.maxBuffer ) {
        this.buffer = _.last( this.buffer, this.maxBuffer );
      }
    });
  };
  
  this.
};

var mooRequest = function( req, command, lineParser, finished ) {
	var moo = net.connect( req.app.get('moo.port') , req.app.get('moo.host'), function() {
		moo.write(command + "\r\n");
	});
	
	moo.on( 'data', 
	function( data ) {
		data = data.toString();
		var lines = data.split(/\r\n/);
		for ( var i = 0; i < lines.length; i++ ) {
			lineParser( moo, lines[i] );
		}
	});
	
	if (finished != null) {
		moo.on( 'end', finished);
	}
};



exports = module.exports;

exports.connect = function( req, username, password, next ) {
  
}

exports.request = function( req, command, lineParser, finished ) {
	if ( finished === undefined ) {
		finished = null;
	}
	mooRequest( req, command, lineParser, finished);
}
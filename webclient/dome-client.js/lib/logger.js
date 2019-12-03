var config  = require('./config'),
	util    = require('util');

var debugEnabled = true;
if ( config.node.mode === 'production' ) {
	debugEnabled = false;
}
	
var instance = {
	// replace this with something more robust for varied messaging
	log: function( type, msg, meta) {
		if ( meta ) {
			console.log( "[" + type + "]", msg, meta );
		} else {
			console.log( "[" + type + "]", msg );
		}
	},
	error: function( type, msg, meta ) {
		if ( meta ) {
			console.error( "[" + type + "]", msg, meta );
		} else {
			console.error( "[" + type + "]", msg );
		}		
	},
	inspect: function( thing ) {
		console.dir( thing );
	}
};

var exports = module.exports;

exports.inspect = function( thing ) {
	if ( debugEnabled ) {
		instance.inspect( thing );
	}
};

exports.log = function( msg, meta ) {
	if ( debugEnabled ) { 
		instance.log('debug', msg, meta );
	}
};

exports.debug = function( msg, meta ) {
	if ( debugEnabled ) { 
		instance.log( 'debug', msg );
		if ( meta ) {
			instance.inspect( meta );
		}
	}
};

exports.info = function( msg, meta ) {
	instance.log( 'info', msg, meta );
};

exports.error = function( msg, meta ) {
	instance.error( 'error', msg);
	if ( meta ) {
		instance.error( util.inspect( meta ) );
	}
};

exports.warn = function( msg, meta ) {
	instance.error( 'warn', msg, meta );
}
/*!
 * config abstraction
 * Make sure you have $NODE_ENV defined with the name of a config in the /config directory.
 */

try {
  var myName = process.env['NODE_ENV'];
  if ( myName ) {
	  var myConfig = require( "../config/" + myName );
	  module.exports = myConfig;
  } else {
    var defaultConfig = require( '../config/default.js' );
    module.exports = defaultConfig;  
  }
} catch ( e ) {
  console.log( e );
  console.log( 'unable to find $NODE_ENV defined configuration, using default' );
  var defaultConfig = require( '../config/default.js' );
  module.exports = defaultConfig;
}

var logger = require( '../lib/logger' ),
    config = require( '../lib/config' ),
    fs     = require( 'fs' );


var AUTOCOMPLETE = {};
var ac = function(usertype, next) {
  if (AUTOCOMPLETE[usertype]) {
    next(null, AUTOCOMPLETE[usertype]);
  } else if (config.autocomplete[usertype]) {
    console.log(config.autocomplete[usertype]);
    fs.readFile(config.autocomplete[usertype], 'utf8', function( err, data ) {
      AUTOCOMPLETE[usertype] = data.split("\n");
      next(null, AUTOCOMPLETE[usertype]);
    });
  } else {
    next(null, []);
  }
};

var exports = module.exports;
exports.basic = function( req, res ) {
  ac(req.params.type, function( err, cmds) { res.json(cmds); });
};
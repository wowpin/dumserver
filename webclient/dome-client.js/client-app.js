var config     = require( './lib/config' ),
    logger     = require( './lib/logger' ),
    io         = require( 'socket.io' ),
    fs         = require( 'fs' ),
    net        = require( 'net' ),
    path       = require( 'path' ),	
    http       = require( 'http' ),
    https      = require( 'https' ),
    engine     = require( 'ejs-locals' ),
    responsive = require('express-responsive'),
    vger       = require( 'version-git' ),
    routes     = {
      'autocomplete' : require( './routes/autocomplete' ),
      'screens'      : require( './routes/screens' ),
      'socket'       : require( './routes/socket' ),
    },
    express    = require( 'express' ),
    app        = express();


var server  = http.createServer( app );
var httpMgr = io.listen( server, function() {
  logger.info("socket.io listening to http");
} );


if ( config.ssl ) {
  var sslOptions = {
    key  : fs.readFileSync(config.ssl.key),
    cert : fs.readFileSync(config.ssl.cert)
  };
  
  if ( config.ssl.ca ) {
    sslOptions['ca'] = fs.readFileSync(config.ssl.ca);
  }

  var sslServer = https.createServer( sslOptions, app );
  var httpsMgr  = io.listen( sslServer, sslOptions, function() {
    logger.info("socket.io listening to https");
  } );
}


app.configure(function () {
  // use ejs-locals for all ejs templates:
  app.engine( 'ejs', engine );
  
  app.set( 'views', __dirname + '/views' );        // where to find the templates for pages
  app.set( 'view engine', 'ejs');                  // ormat the templates are in
  
  // 3 is debug, 2 is info
  httpMgr.set('log level', ( config.node.mode == 'production' ? 1 : 3 ) );
  if ( config.ssl ) {
      httpsMgr.set('log level', ( config.node.mode == 'production' ? 1 : 3 ) );
  }

  var versionHash = process.argv[process.argv.length-1];
  app.set( 'cachingHash', versionHash );
	
	vger.version(config.version.major, config.version.minor, function( err, version ) {
	  app.set('version', version);
	});
	
  
  app.use( function (req, res, next ) {
	  res.header( "X-Powered-By", config.node.poweredBy );
	  next();
	});
	 

	// define req.device as one of desktop tablet phone tv bot
  // It will assume desktop if no user agent string is given,
  // and fallback to phone if the user agent string is unknown.
	app.use( responsive.deviceCapture() );
	
  app.use( express.cookieParser() );
  app.use( express.bodyParser() );
  app.use( express.session( { secret: config.node.session.secret, key: config.node.session.key } ) );
  
  app.use( function( req, res, next ) {
	  // attach a number of values to the app.locals so they're available when we render a template
	  // note that its better to attach a function if the majority of pages will not need the values
	  // the function might return
	  res.app.locals({ 
	    socketUrl    : config.node.socketUrl,
	    socketUrlSSL : config.node.socketUrlSSL,
	    req          : req,
	    session      : req.session,
	    decache      : function(url) { return "" + url + "?" + app.get('cachingHash'); },
	    version      : app.get( 'version' ),
	    poweredBy    : config.node.poweredBy,
	    gameName     : config.moo.name,
      connected    : routes.socket.connected
		});
		next();
	});
	
  app.use( app.router );
    
  // if the request was for CSS, this will compile the less into css and return it
	// note that when node is proxied behind apache, the CSS file may not be compiled naturally
	// in this situation, request the CSS url directly from the node port to force it to be compiled
	app.use( require( 'less-middleware' )({
		dest: __dirname + '/public/css',
		src: __dirname + '/less',
		prefix: '/css',
		compress: true
	}) );
	
	// now we match static resources in /public
  app.use( ({ src: __dirname + '/public' }) );
  app.use( express.static( path.join( __dirname, 'public' ) ) );
  
  // load the player version of the autocomplete file to 
  fs.readFile( config.autocomplete.p, function( err, data ) {
    if ( err ) {
      logger.error( 'error while checking for autocomplete file ', err );
    }
    app.set('autocomplete');
    var vDesc = 'dome-client.js v' + app.get('version');
    if ( config.node['ip'] ) {
      // we'll listen to a specific ip for new connections
      server.listen( config.node.port, config.node.ip, function() {
        logger.info( vDesc +  ' listening on ip ' + config.node.ip + ' and port ' + config.node.port );
      });
      
      if ( config.ssl ) {
        sslServer.listen( config.ssl.port, config.node.ip, function() {
          logger.info( vDesc +  ' listening on ip ' + config.node.ip + ' and port ' + config.ssl.port );  
        });
      }
    } else {
      // no specific ip, we'll listen to all of them
      server.listen( config.node.port, function() {
        logger.info( vDesc + ' listening on port ' + config.node.port );  
      } );
      
      if ( config.ssl ) {
        sslServer.listen( config.ssl.port , function() {
          logger.info( vDesc + ' listening on port ' + config.ssl.port );  
        });
      }
    }
  });
});

httpMgr.sockets.on( 'connection', routes.socket.connection ); // Default connection handler for all websocket requests
if ( config.ssl ) {
    httpsMgr.sockets.on( 'connection', routes.socket.connection );
}
app.get( '/', routes.screens.connect );                // Connection Screen
app.post( '/', routes.screens.connect );
app.get( '/client-options/', routes.screens.options ); // Options Screen
app.get( '/player-client/', routes.screens.client );   // Game Client Screen
app.get( '/editor/:type(basic|basic-readonly|verb)/', routes.screens.editor );  // Editor Windows
app.get( '/channel/:name/', routes.screens.channel ); // filtered content channel template
app.get( '/ac/:type(p)', routes.autocomplete.basic );        // Fetch autocomplete terms
app.post( '/save/:filename', function( req, res, next ) {
  res.setHeader('Content-disposition', 'attachment; filename=' + req.params.filename);
  res.setHeader('Content-type', 'text/html');
  res.write('<html><head><title>Web Client Buffer</title>');
  res.write('<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Source+Code+Pro|Quantico:400,400italic,700">');
  res.write('<base href="http://moo.sindome.org">');
  res.write('<link rel="stylesheet" type="text/css" href="http://www.sindome.org/css/dome.css">');
  res.write('<link rel="stylesheet" tyle="text/css" href="http://moo.sindome.org/css/client.css">');
  res.write('</head><body><div id="browser-client"><div id="lineBuffer">');
  res.write(req.body.buffer);
  res.write('</div></div></body></html>');
  res.end();
});

process.on('uncaughtException', function(err) {
    // handle the error safely
    console.log(err);
    
});
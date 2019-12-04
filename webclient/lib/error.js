var logger = require( './logger' );


var metrics = {
	'403' : {
		count: 0,
		urls: [],
		ips: []
	},
	'404' : {
		count: 0,
		urls: [],
		ips: []
	},
	'500' : {
		count: 0,
		urls: [],
		ips: []
	}
};

var serveError = function( status, req, res, page ) {
	metrics[status].count++;
	metrics[status].urls.push(page.url); // add to back
	metrics[status].ips.push(req.header('X-Forwarded-For'));
	console.log(metrics[status].urls.length);
	if (metrics[status].urls.length >= 20 ) {
		metrics[status].urls.shift(); // remove from front
		metrics[status].ips.shift();
	}
	res.status( status );
	res.render( 'errors/' + status, page );
}
 
var exports = module.exports;
exports.metrics = metrics;
exports.permissionDenied = function( req, res, next ) {
	var page = {
		title: 'Permission Denied',
		meta_title : 'Permission Denied',
		meta_description: 'Whoa! You can\'t just go using things without permission!',
		meta_keywords: '403, Permission Denied',
		url: req.url
	};
	console.dir(page);
	serveError( 403, req, res, page );
}

exports.notFound = function( err, req, res, next ) {
	if ( err && err.message == '404' ) {
		console.dir( err );
		var page = {
			title: 'File Not Found',
			meta_title : 'Not Found',
			meta_description : 'The file requested doesn\'t exist.',
			meta_keywords : '404',
			error : err,
			url: req.url
		};
		serveError( 404, req, res, page );
	} else if ( err ) {
		next( err );
	} else {
		next();
	}
}

exports.errorHandler = function( err, req, res, next ) {
	if ( err ) {
		logger.error( 'Unexpected Error Encountered from ' + req.url, err );
		var page = {
			title : 'Unexpected Error',
			meta_title : 'Unexpected Error',
			meta_description : 'Who really expects an error, anyway?',
			meta_keywords : '500',
			error : err,
			url: req.url
		};
		serveError( 500, req, res, page );
	} else {
	  var page = {
			title: 'File Not Found',
			meta_title : 'Not Found',
			meta_description : 'The file requested doesn\'t exist.',
			meta_keywords : '404',
			error : err,
			url: req.url
		};
		serveError( 404, req, res, page );
		next();
	}
}
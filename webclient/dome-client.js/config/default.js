module.exports = {
  'node' : {
    'mode'         : 'production',
// do you want your webclient to allow users to connect to any game => true
// do you want your webclient to connect users only to your game => false
    'connectAnywhere': false,

// if you set this to port 80, you must run the server as root
    'port'         : 80,

// specific ip is optional (if your server has more than one)
//    'ip'           : '208.52.189.89',

    'socketUrl'    : 'http://35.246.211.163:80',
    'socketUrlSSL' : '',
    'poweredBy'    : 'dome-client.js',
    'session'      : {
        'secret' : 'secret',
        'key'    : 'express.sid'
    }
  },
  
// ssl is optional
//  'ssl' : {
//    'port' : 443,
//    'key'  : 'config/ssl/BlahBlah.key',
//    'cert' : 'config/ssl/BlahBlah.crt',
//    'ca'   : 'config/ssl/intermediate.crt'
//  },

  // where it connects to
  'moo' : {
    'name' : 'DUM',
    'host' : '35.246.211.163',
    'port' : 35123
  },

  // specialized autocomplete for each player class
  'autocomplete' : {
    'p' : 'config/ac/player.txt'
  },
  'version' : {
    'major' : '1',
    'minor' : '2'
    // build is pulled from git hash
  }
};

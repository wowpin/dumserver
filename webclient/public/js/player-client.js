
$(document).keydown(function(e){ 
    var elid = $(document.activeElement).is("input:focus, textarea:focus"); 
    if(e.keyCode === 8 && !elid){ 
       return false; 
    }; 
});

var socket = null;
$(document).ready(function(){
  /***************************** setup variables *****************************/
  
  // this is needed because the 'resize' event fires inappropriately in iOS
  var iOS = ( navigator.userAgent.match(/(iPad|iPhone|iPod)/g) ? true : false );
  
  // references to various objects
  var dome = {
    socket          : null,
    titleBarText    : null,
    gameHostname    : 'moo.sindome.org',
    gamePort        : 5555,
    client          : $('#browser-client'),
    buffer          : $('#lineBuffer'),
    statusDisplay   : $('#status'),
    inputReader     : $('#inputBuffer'),
	statusPanel     : $('#statusPanel'),
    reconnectButton : $('#button-reconnect'),
    saveButton      : $('#button-save, #button-save-mini'),
    scrollButton    : $('#button-auto-scroll'),
    clearButton     : $('#button-clear-buffer'),
    closeAllButton  : $('#button-closeall'),
    disconnectView  : {
      overlay     : $('#disconnect-overlay'),
      buttonGroup : $('.disconnect-buttons')
    },
    spawned         : [],
    alert           : {
      tone       : new Audio("/notice.wav"),
      pattern    : null,
      active     : false,
      titleProc  : null  
    }
    
  };  
  
  var setFadeText = function(elem, msg) {
    msg=msg.toUpperCase();
    elem.stop(true, true).text(msg).animate({"opacity":"1"}, 500);
    if (arguments.length > 2 && arguments[2]) {
      // 3rd argument tells it to persist
      return;
    }
    elem.delay(5000).animate({"opacity": "0"}, 1000);
  };
  
  var commandBuffer  = store.get('my-input-buffer') || [];
  var lastInput   = '';
  var commandPointer = commandBuffer.length || -1;
  var client        = dome.client;
  var buffer        = dome.buffer;
  var statusPanel   = dome.statusPanel
  var statusDisplay = dome.statusDisplay;
  var inputReader   = dome.inputReader;  
  var userType      = "p";
  
  var options = window.location.search || null;
  // user preferences
  var preferences   = {
    commandSuggestions : true,
    autoScroll         : 'dbl',
    edittheme          : 'twilight',
    lineBufferFont     : 'standard'
  };
  if (options) {
    if (options.indexOf('cs=false') != -1) {
      preferences.commandSuggestions = false;
    }
  
    if (options.indexOf('as=long') != -1) {
      preferences.autoScroll = 'long';
    }

    if ((ghIndex = options.indexOf('gh=')) != -1) {
      var rest = gh = options.substr(ghIndex);
      if ((n = rest.indexOf("&")) != -1) {
        gh = rest.substr(0, n);
      }
      if (gh.length > 3) {
        dome.gameHostname = gh.substr(3);
      }
    }

    if ((gpIndex = options.indexOf('gp=')) != -1) {
      var rest = gp = options.substr(gpIndex);
      if ((n = rest.indexOf("&")) != -1) {
        gp = rest.substr(0, n);
      }
      if (gp.length > 3) {
        dome.gamePort = gp.substr(3);
      }
    }
  
    if ((ofIndex = options.indexOf('of=')) != -1) {
      var rest = of = options.substr(ofIndex);
      if ((n = rest.indexOf("&")) != -1) {
        of = rest.substr(0,n);
      }
      if (of.length > 3) {
        var font = of.substr(3);
        if (_.contains(FONT_CHOICES, font)) {
          preferences.lineBufferFont = font;
          dome.buffer.removeClass('standardFont').addClass(font + 'Text');
        }
      }
    }
  
    if ((etIndex = options.indexOf('et=')) != -1) {
      var rest = et = options.substr(etIndex);
      if ((n = rest.indexOf("&")) != -1) {
        et = rest.substr(0,n);
      }
      if (et.length > 3) {
        var theme = et.substr(3);
        if (_.contains(EDIT_THEMES, theme)) {
          preferences.edittheme = theme;
        }
      }
    }
  }
  
  /**************************** end variable setup ***********************************/
  
  /**************************** editor functions *************************************/
  // we use this object to load a local editor over several socket events
  var editor = {};
  var editorInit = function() {
    editor = {
       readingContent : false,
       buffer : '',
       editorName : '',
       uploadCommand : ''
     };
  }
  editorInit();

  // analyze the editor properties to determine which editor
  var makeEditor = function(editor) {
    // if there is no upload command, its a read only editor
    var type = "basic-readonly";
    if (editor.uploadCommand ) {
      if (editor.uploadCommand.indexOf("@program") != -1) {
        // verb editor
        type = "verb";
      } else {
        // theres some other command
        type = "basic";
      }
    }
    
    // strip leading linebreaks
    editor.buffer = editor.buffer.replace(/^\n/, '').replace(/[\r\n]+$/, '');
    
    var windowConfig = 'width=640,height=480,resizeable,scrollbars';
    var editWindow = window.open('/editor/' + type + '/?et=' + preferences.edittheme + '&ts=' + (new Date()).getTime(), '' + editor.editorName, windowConfig);
    editWindow.editorData = editor;
    editWindow.uploadSocket = socket;
    editWindow.parentWindow = window;
    editWindow.focus();
 
    return editWindow;
  };
  /******************************************* end editor functions *************************************/
  
  var pauseBuffer = false;
  var pausedLines = 0;
  var STATE_ENUM = {
    RECONNECT_FAILED : -1, // we tried a number of times and gave up
        DISCONNECTED :  0, // we lost connection
           CONNECTED :  1, // we have a connection
        BEFORE_FIRST :  2, // we have yet to try for a connection
  };
  var currentState = STATE_ENUM.BEFORE_FIRST;
  socket = dome.socket = null;
  
  window.getSocket = function() { return socket; } // for our editor windows
  var onUnloadHandler = function() { socket.emit('input', "@quit\r\n"); };
  var onFocusHandler = function() { 
    dome.alert.active = false;
    if (dome.alert.titleProc != null) {
      window.clearInterval(dome.alert.titleProc);
      dome.alert.titleProc = null;
      document.title = dome.titleBarText;
    } 
    if (inputReader) { 
      inputReader.focus(); 
    }
  };
  var onBlurHandler = function() { dome.alert.active = true; };
  var onErrorHandler = function(e) { if (console) { console.log(e); } if (statusDisplay) { setFadeText(statusDisplay, 'ERROR RECEIVED: ' + e, true); } };
  
  var onResizeHandler = function() {
    dome.client.css('height', '' + (window.innerHeight) + 'px');
    dome.buffer.css('height', '' + (window.innerHeight - 75) + 'px');
  };
  var onDisconnectedHandler = function() {
    currentState = STATE_ENUM.DISCONNECTED;
    editor.readingContent = false;
    if ( statusDisplay ) { setFadeText(statusDisplay, 'DISCONNECTED AT ' + (new Date()).toString(), true); }
    dome.disconnectView.overlay.removeClass('hide');
    dome.disconnectView.buttonGroup.removeClass('hide');
  };
  var onReconnectHandler = function() {
    dome.disconnectView.overlay.addClass('hide');
    dome.disconnectView.buttonGroup.addClass('hide');
  };
  var onReconnectFailedHandler = function() {
    currentState = STATE_ENUM.RECONNECT_FAILED;
    dome.disconnectView.overlay.removeClass('hide');
    dome.disconnectView.buttonGroup.removeClass('hide');
  };
  
  var titleAlerted = false;
  var alertTitle = function() {
    if (!titleAlerted) {
      document.title = "!! " + dome.titleBarText;
      titleAlerted=true;
    } else {
      document.title = dome.titleBarText;
      titleAlerted=false;
    }
  };
  
  var onAlert = function() {
    if (dome.alert.titleProc != null) {
      return;
    }
    
    dome.alert.titleProc = window.setInterval(alertTitle, 500);
  };
  
  var onConnectedHandler = function() {
    if (currentState == STATE_ENUM.DISCONNECTED) {
      onReconnectHandler();
    }
    currentState = STATE_ENUM.CONNECTED;
    inputReader[0].focus(); // focus the cursor in the input field
    setFadeText(statusDisplay, 'CONNECTED AT ' + (new Date()).toString());
    if (!initialCommand)
    setTimeout(function() {
      // delayed input to account for latency
      var cmd;
      if ((cmd = store.get('dc-initial-command'))) {
        // guest login
        document.title = dome.titleBarText = "Guest | " + gameName + " | " + poweredBy;
        socket.emit('input', cmd, function(response) {
          store.remove('dc-initial-command');
        });
      } else if ((cmd = store.get('dc-user-login'))) {
        // user login
        var who = store.get('last-username');
        dome.alert.pattern = new RegExp(who);
        document.title = dome.titleBarText = who + " | " + gameName + " | " + poweredBy;
        console.log('logging into moo with command ' + cmd);
        socket.emit('input', cmd, function(response) {
          //
        });
      }
    }, 2000);
    initialCommand = true;
  };
  
  var getCursorPosition = function(textarea) {
    if ("selectionStart" in textarea) {
       return {
         start: textarea.selectionStart,
         end: textarea.selectionEnd
       };
    } else {
      // really just IE 
      return { start: 1, end: 1 };
    }
  };
  
  var winJQ = $(window);
  winJQ.on('focus', onFocusHandler);
  winJQ.on('blur', onBlurHandler);
  if (!iOS) {
    winJQ.on('resize', onResizeHandler);
  }
  winJQ.on('orientationchange', onResizeHandler);
  winJQ.on('unload', onUnloadHandler);
  
  
  var initialCommand = false;
  
  var onLoadHandler = function() {
    socket = dome.socket = io.connect(('https:' == document.location.protocol ? socketUrlSSL : socketUrl), {
      'query' : 'host=' + dome.gameHostname + '&port=' + dome.gamePort,
      'sync disconnect on unload' : true // send 'disconnect' event when the page is left
    });
    
    socket.on('connected', function( data ) {
      onConnectedHandler();
    });
    socket.on('disconnect', function( data ) {
      onDisconnectedHandler();
    });
    socket.on('reconnect_failed', function( data ) {
      onReconnectFailedHandler();
    });
    socket.on( 'error', function(e) {
      onErrorHandler(e);
    });
    
    console.log("onLoadHandler socket");
    console.log(socket);
  };
  
  onResizeHandler();
  onLoadHandler();

  /*************************** content from the remote server ***********************/
  socket.on( 'data', function( segment ) {
    // a segment is one or more lines
    // #$# edit name: Note: testing upload: @@set_note 12106
    if ( editor.readingContent ) {
      var terminalMarker = segment.lastIndexOf("\n.\r");
      if ( terminalMarker != -1 || (terminalMarker = segment.indexOf(".\r\n")) == 0 ) {
        editor.buffer += segment.substr(0, terminalMarker);
        var spawned = makeEditor( editor );
        if (spawned) {
          dome.spawned[dome.spawned.length] = spawned;
        }
        editorInit();
        segment = segment.substr(terminalMarker+4);
      } else {
		editor.buffer += segment; 
		segment = '';
      }
    }
    if ((meta = segment.indexOf('#$#')) != -1) {
      var end = segment.indexOf( "\r\n", meta );
      var metaCommand = segment.substr(meta, end - meta);
      var a = metaCommand.split(' upload: ');
      var uploadCommand = a[a.length-1];
      a = a[0].split(' name: ');
      var editorName = a[a.length-1];
      metaCommand = a[0].substr(4);
      if ( metaCommand == "edit" ) {
        editorInit();
        var terminalMarker = segment.indexOf("\n.\r", end);
        if ( terminalMarker != -1 ) {
          dome.spawned[dome.spawned.length] = makeEditor( { 'editorName' : editorName, 'uploadCommand' : uploadCommand, 'buffer' : segment.substr( end + 1, terminalMarker - end ) } );
          segment = segment.substr(0, meta) + segment.substr(terminalMarker);
        } else {
          // the rest of this will finish in another event
          editor.readingContent = true;
          editor.buffer += segment.substr(end + 1);
          editor.editorName = editorName;
          editor.uploadCommand = uploadCommand;
          segment =  segment.substr(0, meta); // remove the start of the edit buffer from the segment
        }
      } else if ( metaCommand && metaCommand.indexOf("user") == 0) {
        // global within closure
        userType = a[0].substr(a[0].indexOf("user-type"), 12).split(" ")[1];
        segment = segment.substr(0, meta) + segment.substr(meta + a[0].length);
        if (!window.location.query || window.location.query.indexOf('ac=no') != -1) {
          var autoCommands = [];
          $.ajax({
            url: ('/ac/' + userType + '/'),
            dataType: 'json',
            success: function(data) {
              autoCommands = data;
              inputReader.autocomplete({ 
                minLength: 2,
                position: { my: 'left bottom', at: 'left bottom', of: "DIV#lineBuffer", offset: "10 -90" }, 
                source: autoCommands 
              });
            }
          });
        }
      } else {
        if (console) {
          console.log( 'unhandled meta command: ' + metaCommand );
        }
      }
      // end of #$# meta command reader
    }
    
    _.each( subs, function( sub, subIndex ) {
      segment = segment.replace( sub.pattern, sub.replacement );
    });
    
    // make links clickable
    segment = segment.replace(urlRegex, function(url) {  
      return '<a href="' + url + '" target="_new">' + url + '</a>';  
    });
      
    if (dome.alert.active && dome.alert.pattern != null) {
      if (segment.match(dome.alert.pattern, "i")) {
        dome.alert.tone.play();
        onAlert();
      }
    }
    //buffer.append( lastInput );
	//if (String(segment).includes('<c3RhdHVzcGFuZWw=>') == true) {
	if ( segment.indexOf('c3RhdHVzcGFuZWw') > -1 ) {
		statusPanel.html('');
		//segment = segment.substring(18);
		//statusPanel.append( segment.substring(25) );
		var statusPanelContents = segment.substring(16).split(';');
		//statusPanel.append( String( typeof statusPanelContents ) );
		//statusPanel.append( "\n" + statusPanelContents );
		//var index;
		//for (index = -1; index < statusPanelContents.length; ++index) {
			//statusPanel.append( "<" + statusPanelContents[index] + ">" );
		//}
		var intHP = parseInt(statusPanelContents[3], 10);
		var intHPMax = parseInt(statusPanelContents[4], 10);
		var intCharge = parseInt(statusPanelContents[5], 10);
		var intChargeMax = parseInt(statusPanelContents[6], 10);
		
		statusPanel.append( "<br><br>" ); 

		//statusPanel.append( statusPanelContent[5] + "<br>" );
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>     :    " + String(statusPanelContents[0]) + "" );
		statusPanel.append( "<br>" );                                          
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;Lvl&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>      :    " + String(statusPanelContents[1]) + "" );
		statusPanel.append( "<br>" );            
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;Location&nbsp;&nbsp;</span>  :    " + String(statusPanelContents[2]) + "" );
		statusPanel.append( "<br>" );    

		if ( intHP > 0 ) {
			var tableSrc = "<table height='6'><tr><td width='13px'></td><td bgcolor='#000000' width='96px'><table border='0' width='96px'><tr><td width='" + String(intHP / intHPMax * 100) + "' bgcolor='#22a318'></td><td width='auto' bgcolor='#000000'></td></tr></table></td></tr></table>";
		}
		else {
			var tableSrc = "<table height='6'><tr><td width='13px'></td><td bgcolor='#000000' width='96px'><table border='0' width='96px'><tr><td width='" + String(intHP / intHPMax * 100) + "' bgcolor='#000000'></td><td width='auto' bgcolor='#000000'></td></tr></table></td></tr></table>";
		}
		

		statusPanel.append( "<br>" );
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;HP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>        :    " + String(statusPanelContents[3]) + " / " + String(statusPanelContents[4]) + "" );
		statusPanel.append( tableSrc );
		statusPanel.append( "<br>" );    

		var tableSrc = "<table height='6'><tr><td width='13px'></td><td bgcolor='#000000' width='96px'><table border='0' width='96px'><tr><td width='" + String(intCharge / intChargeMax * 100) + "' bgcolor='#22a318'></td><td width='auto' bgcolor='#000000'></td></tr></table></td></tr></table>";
		
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;Charge&nbsp;&nbsp;&nbsp;&nbsp;</span>    :    " + String(statusPanelContents[5]) + " / " + String(statusPanelContents[6]) + "" );
		statusPanel.append( tableSrc );
		statusPanel.append( "<br>" );            
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;In Combat&nbsp;</span> :    " + String(statusPanelContents[7]) + "" );
		statusPanel.append( "<br>" );            
		statusPanel.append( "&nbsp;&nbsp;<span class='xterm256-bg-BlueMostlyDark'>&nbsp;Target&nbsp;&nbsp;&nbsp;&nbsp;</span>    :    " + String(statusPanelContents[8]) + "" );
	}
	else {
		buffer.append( segment );
	}
	//statusPanel.html('');
	//statusPanel.append ( segment );
    
    if (pauseBuffer) {
      pausedLines++;
      setFadeText(statusDisplay, "" + pausedLines + " new lines, double click to reenable auto scroll.");
    } else {
      buffer.animate( { scrollTop : buffer[0].scrollHeight }, 50 );
    }
  });
  
  /******************* auto scroll via double click or long click *******************/
  var longClickProc = null;
  var longPressed = false;  
  var onToggleAutoScroll = function( event ) {
    longClickProc = null; // clears the process variable if this was a long click
    window.getSelection().removeAllRanges();
    if (pauseBuffer) {
      pauseBuffer = false;
      pausedLines = 0;
      setFadeText(statusDisplay, "Auto scroll reenabled.");
      buffer.animate( { scrollTop: buffer[0].scrollHeight }, 50 );
      buffer.removeClass("scroll-disabled");
      dome.scrollButton.html('PAUSE SCROLL');
    } else {
      pauseBuffer = true;
      setFadeText(statusDisplay, "Auto scroll disabled, " + (preferences.autoScroll != 'long' ? "double click" : "long click") + " to reenable.");
      buffer.addClass("scroll-disabled");
      dome.scrollButton.html('RESUME SCROLL');
    }
  };

  if (preferences.autoScroll != 'long') {
    // double click is the default method for auto scroll
    buffer.on( 'dblclick', onToggleAutoScroll);
  } else {
    // long click support is available here
    buffer.on( 'mousedown', function( event ) {
      longClickProc = window.setTimeout(onToggleAutoScroll, 2000);
    });
    buffer.on( 'mouseup', function( event ) {
      if (longClickProc != null) {
        window.clearTimeout(longClickProc);
      }
      longClickProc = null;
    })
  }
  /******************* end AUTO SCROLL  *******************/
  
  /************ clicking a channelable line ************/
  buffer.on( 'click', function( event ) {
    console.log("click event handler triggered");
    var elem = $(event.target);
    if (elem.hasClass("filterable")) {
      onClickedChannel(elem);
    }
  });
  
  /**************** inputreader is optional **************/ 
  if ( inputReader ) {
    inputReader.on( 'keydown', function( event ) {
       if ( event.which == 38 && commandPointer >= 0 ) {
         // up (show next oldest)
         var cursor = getCursorPosition(inputReader[0]);
         if (cursor.start != cursor.end) {
           // text is selected
         } else {
           if (cursor.start < 150) {
             // is the cursor 'near' the top
             commandPointer = ( commandPointer <= -1 ? commandBuffer.length : commandPointer ) - 1;
             inputReader.val(commandBuffer[commandPointer]);
             event.preventDefault();
           } else {
             // let the cursor move up, hopefully?
           }
         }
         
         return false;
       } else if ( event.which == 40 && commandPointer < commandBuffer.length - 1 ) {
         // down (show next newest)
         commandPointer = ( commandPointer + 1 > commandBuffer.length ? 0 : commandPointer) + 1 ;
         inputReader.val(commandBuffer[commandPointer]);
         event.preventDefault();
         return false;
       } else if ( event.which == 40 && commandPointer >= commandBuffer.length -1 ) {
         // down (at last, don't show me anything)
         commandPointer = commandBuffer.length;
         if (inputReader.val() == lastInput) {
           inputReader.val('');
           lastInput = '';
         } else {
           inputReader.val(lastInput);  
         }
         event.preventDefault();
         return false;
       }
    });
     inputReader.on( 'keypress' , function( event ) {
       if ( event.which == 8 ) {
         
       }
       if ( event.which == 13 && !event.shiftKey ) {
         inputReader.autocomplete( "close" );
         // enter key
         event.preventDefault();
         socket.emit('input', inputReader.val(), function( state ) {
           setFadeText( statusDisplay, state.status, false );
           commandBuffer[commandBuffer.length] = inputReader.val();
           if (commandBuffer.length > 2000) {
             commandBuffer.shift();
           }
           commandPointer = commandBuffer.length;
           store.put('my-input-buffer', commandBuffer) // localStore deals in strings, this won't work as an array Chad. - Future Chad
           inputReader.val('');
           lastContent = '';
         });
         return false;
       } else {
         setTimeout(function() { lastInput = inputReader.val(); }, 5);
       }
     });
     inputReader.on( 'focus' , function() {
       //console.log('focused on the input reader');
     });
     
     if (!preferences.commandSuggestions) {
        // ?ac=no to disable autocomplete
      } else {
        var autoCommands = [];
        $.ajax({
          url: '/ac/' + userType,
          dataType: 'json',
          success: function(data) {
            autoCommands = data;
            inputReader.autocomplete({ 
              delay: 10,
              minLength: 2,
              position: { my: 'left bottom', at: 'left bottom', of: "DIV#lineBuffer", offset: "10 -90" }, 
              source: autoCommands 
            });
          }
        });
      }
   }
   
   if ( dome.reconnectButton ) {
     dome.reconnectButton.on('click', function() {
       window.location.reload();
     });
   }
   
   if ( dome.saveButton ) {
     dome.saveButton.on('click', function() {
       var now = new Date();
       timestamp = "" + (now.getMonth()+1) + now.getDate() + now.getFullYear() + now.getHours() + now.getMinutes();
       var form = $('#save-form');
       form.attr('action', '/save/buffer.' + timestamp + '.html');
       $('input', form).val(dome.buffer.html());
       form.submit();
     });
   }
   
   if ( dome.clearButton ) {
     dome.clearButton.on('click', function() {
       dome.buffer.html('');
     });
   }
   
   if ( dome.scrollButton ) {
     dome.scrollButton.on('click', onToggleAutoScroll);
   }
   
   if ( dome.closeAllButton ) {
     dome.closeAllButton.on('click', function() {
       for (var i = 0; i < dome.spawned.length; i++) {
         if (dome.spawned[i]) {
           dome.spawned[i].close();
         }
       }
       for (var i = 0; i < dome.channels.length; i++) {
         if (dome.channels[i]['window']) {
           dome.channels[i].window.close();
         }
       }
       window.close();
     });
   }
});
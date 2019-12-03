
var isReadOnly = function(cmd) {
  return (cmd == "none" || !cmd);
}

$(document).ready(function(){
  
  var data = window.editorData;
  if ( data == null ) {
    data = { 'editorName' : 'Scratch', 'uploadCommand' : 'none', 'buffer' : '' };
  }
  
  var uploadCommand = data.uploadCommand;
  var editorName = data.editorName;
  var buffer = data.buffer;
  var initialValue = buffer;
  
  var cta = $('button.upload');
  var abort = $('button.abort');
  var basicEditor = $('div.editor textarea');
  
  if ( verbEditor != null )  {
    verbEditor.setValue(buffer);
    initialValue = verbEditor.getValue();
  } else if ( basicEditor != null && basicEditor.length > 0 ) {
    basicEditor.text(buffer);
    initialValue = basicEditor.val();
  }
  
  // initial setup
  document.title = (isReadOnly(uploadCommand) ? 'Viewing ' : 'Editing ') + editorName;
  cta.html(uploadCommand);
  
  // upload button
  if ( cta && cta.length >= 1) {
    cta.click(function() {
      if (isReadOnly(uploadCommand)) {
        return;
      }
      //alert(editor.val());
      //var socket = window.uploadSocket;
      var socket = window.parentWindow.getSocket();
      socket.emit('input', uploadCommand, function( state ) {
        var uploadData = '';
        if ( verbEditor != null ) {
          uploadData = verbEditor.getValue();
        } else {
          uploadData = basicEditor.val();
        }
        socket.emit('input', uploadData + "\n.", function( state ) {
          initialValue = uploadData;
        });
      });
    });
  }
  
  // abort or close button
  if ( abort && abort.length >= 1) {
    abort.on('click', function() {
      var val = (verbEditor != null ? verbEditor.getValue() : basicEditor.val());
      if (val == initialValue || window.confirm('Abort editing and lose your changes?')) {
        window.close();
      }
    });
  }
});
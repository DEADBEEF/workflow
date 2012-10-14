// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submit(action, method, values) {
    var form = $('<form/>', {
        action: action,
        method: method
    });
    $.each(values, function() {
        form.append($('<input/>', {
            type: 'hidden',
            name: this.name,
            value: this.value
        }));    
    });
    form.appendTo('body').submit();
}

$(document).ready(function () {
    $("#dialog").dialog({
        autoOpen: false,
        modal:true,
        bgiframe: true,
        width: 300,
        height:150
    });
    // Create jqxTree 
    var theme = getTheme();
    // create jqxTree
    $('#jqxTree').jqxTree({ height: '300px', hasThreeStates: true, checkboxes: true, width: '500px', theme: theme });
    $('#jqxCheckBox').jqxCheckBox({ width: '200px', height: '25px', checked: true, theme: theme });
    $('#jqxCheckBox').bind('change', function (event) {
        var checked = event.args.checked;
        $('#jqxTree').jqxTree({ hasThreeStates: checked });
    });
    $("#file-submit").click(function () {
      var items = $("#jqxTree").jqxTree('getItems');
      var data = Array();
      var regex = /id="(\d+)"/;
      $.each(items, function () {
          if (!this.hasItems) {
            var value=this.originalTitle.match(regex)[1];
            if (this.checked) {
              data.push({name:"input_files", value:value});
            }
          }
      });
      data.push({name:"assignee", value:$("#id_assignee").val()});
      data.push({name:"priority", value:$("#id_priority").val()});
      data.push({name:"output_folder", value:$("#id_output_folder").val()});
      var csrftoken = getCookie('csrftoken');
      data.push({name:"csrfmiddlewaretoken", value:csrftoken});
      submit('.', 'POST', data);
      //alert(data);

      
    });
  
});
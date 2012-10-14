

$(document).ready(function () {
    // Create jqxTree 
    var theme = getTheme();
    $('#jqxTree').jqxTree({ height: '300px',  width: '500px', theme: theme });
    $('#jqxCheckBox').jqxCheckBox({ width: '200px', height: '25px', checked: true, theme: theme });
    $('#jqxCheckBox').bind('change', function (event) {
        var checked = event.args.checked;
        $('#jqxTree').jqxTree({ hasThreeStates: checked });
    });


});

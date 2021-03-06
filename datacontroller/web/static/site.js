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


function show_user() {
    $("#server").addClass("hidden");
    $("#user").removeClass("hidden");
    $("#user_but").addClass("hidden");
    $("#server_but").addClass("hidden");
}

function show_server() {
    $("#server").removeClass("hidden");
    $("#user").addClass("hidden");
    $("#user_but").addClass("hidden");
    $("#server_but").addClass("hidden");


}

function show_jobs() {
    $("#jobs").toggleClass("hidden");
}

function show_category() {
    $("#category").toggleClass("hidden");
}

function populate_job(job_id) {
    // Do a get to fetch job details
    //
    $.get('../../getjob/?job_id=' + job_id ,function (data) {
        if (data["type"] == "3"){
            $("#server_job_div").addClass('hidden');
            $("#user_job_div #id_type").val(data["type"]);
            $("#user_job_div #id_category").val(data["category"]);
            $("#user_job_div #id_id").val(data["id"]);
            $("#user_job_div #id_name").val(data["name"]);
            $("#user_job_div #id_description").val(data["description"]);
            $("#user_job_div").removeClass('hidden');
        } else {
            $("#user_job_div").addClass('hidden');
            $('#server_job_div input:radio[name=type]')[parseInt(data["type"])-1].checked = true;
            $("#server_job_div #id_id").val(data["id"]);
            $("#server_job_div #id_category").val(data["category"]);
            $("#server_job_div #id_name").val(data["name"]);
            $("#server_job_div #id_description").val(data["description"]);
            $("#server_job_div #id_script").val(data["script"]);
            $("#server_job_div").removeClass('hidden');
        }
        //alert(data["name"]);

   });

}

function add_user_job() {
   $.get('../../addjob/?job_type=3' ,function (data) {
        $("#server_job_div").addClass('hidden');
        $("#user_job_div #id_type").val(data["type"]);
        $("#user_job_div #id_category").val(-1);
        $("#user_job_div #id_id").val(data["id"]);
        $("#user_job_div #id_name").val(data["name"]);
        $("#user_job_div #id_description").val("");
        $("#user_job_div").removeClass('hidden');
        //alert(data["name"]);

   });
}

function add_server_job() {
   $.get('../../addjob/?job_type=1' ,function (data) {
        $("#user_job_div").addClass('hidden');
        $('#server_job_div input:radio[name=type]')[0].checked = true;
        $("#server_job_div #id_type").val(data["type"]);
        $("#server_job_div #id_id").val(data["id"]);
        $("#server_job_div #id_category").val(-1);
        $("#server_job_div #id_name").val(data["name"]);
        $("#server_job_div #id_description").val("");;
        $("#server_job_div #id_script").val("");
        $("#server_job_div").removeClass('hidden');
        //alert(data["name"]);

   });
}

function add_cat() {
    $("#cat_div").removeClass("hidden");
};

function cancel_user() {
    $("#user").addClass("hidden");
    $("#server").addClass("hidden");
    $("#user_but").removeClass("hidden");
    $("#server_but").removeClass("hidden");
}
function start_scan() {
    var csrftoken = getCookie('csrftoken');
    var url = location.pathname.split("/");
    var site = "";
    if (url[1] == "site"){
      site = url[url.length - 2];
    } else if (url[1] == "edit"){
      site = url[url.length - 3];
    }
    values = [ {"name": "site", "value":site}, {"name":"csrfmiddlewaretoken", "value":csrftoken}]
    submit("../../../../../startScan/","POST", values)
  
}

$(document).ready(function () {
    $("#dialog").dialog({
        autoOpen: false,
        modal:true,
        bgiframe: true,
        width: 300,
        height:150
    });
    $("#dialog2").dialog({
        autoOpen: false,
        modal:true,
        bgiframe: true,
        width: 300,
        height:150
    });
    // Create jqxTree 
    var theme = getTheme();
    // create jqxTree
    $('#jqxTree').jqxTree({ height: '300px', width: '500px', theme: theme });
    $('#jqxCheckBox').jqxCheckBox({ width: '200px', height: '25px', checked: true, theme: theme });
    $('#jqxCheckBox').bind('change', function (event) {
        var checked = event.args.checked;
        $('#jqxTree').jqxTree({ hasThreeStates: checked });
    });
    $("#user_but").click(show_user);
    $("#server_but").click(show_server);
    $("#view_job").click(show_jobs);
    $("#view_category").click(show_category);
    $("#add_user_job").click(add_user_job);
    $("#add_server_job").click(add_server_job);
    $("#cat_but").click(add_cat);
    $("#user_cancel").click(cancel_user);
    $("#server_cancel").click(cancel_user);
    $("#btn-start-scan").click(start_scan);

});

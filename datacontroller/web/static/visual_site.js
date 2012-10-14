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

function connections(params) {
    if (params["sourceId"] == params["targetId"]){
        return false;
    }
    var connections = jsPlumb.getConnections();
    for (i = 0; i < connections.length; ++i) {
        if (connections[i]["sourceId"] == params["sourceId"] &&
            connections[i]["targetId"] == params["targetId"]){
            return false;
        }
    }
    var csrftoken = getCookie('csrftoken');
    var url = location.pathname.split("/");
    var site = "";
                if (url[1] == "site"){
                  site = url[url.length - 2];
                } else if (url[1] == "edit"){
                  site = url[url.length - 3];
                }
    //alert(csrftoken);
    var addEdge = true;
    $.ajax({
              url :"../../../addDep/",
              type: "post",
              async: false,
              data:  {  csrfmiddlewaretoken: csrftoken,
                         sourceId:params["sourceId"],
                         targetId:params["targetId"],
                         site:site},
              success: function(data) {
                              if (data == "good") {
                                 addEdge = true;
                              } else {
                                  alert("Edge cannot be added, cycle detected");
                                  addEdge = false;
                              }
                            }
              });
                       
    return addEdge  ;
}

function deleteConnection(connection) {
    if (window.getSelection)
                window.getSelection().removeAllRanges();
        else if (document.selection)
                    document.selection.empty();
    $("#dialog").dialog({
        buttons: {
            "Confirm" : function() {
                $(this).dialog("close");
                var csrftoken = getCookie('csrftoken');
                var url = location.pathname.split("/");
                var site = "";
                if (url[1] == "site"){
                  site = url[url.length - 2];
                } else if (url[1] == "edit"){
                  site = url[url.length - 3];
                }

                $.post("../../../removeDep/", {  csrfmiddlewaretoken: csrftoken,
                         sourceId:connection["sourceId"],
                         targetId:connection["targetId"],
                         site:site},
                            function(data) {
                                jsPlumb.detach(connection);
                            });
            },
            "Cancel" : function () {
                $(this).dialog("close");
            }
        }
    });
    $("#dialog").dialog("open");

}
function drop_alert() {
    var id = this.id;
    var position = $(this).position();
    var csrftoken = getCookie("csrftoken")
    $.post("../../../placeNode/", {  csrfmiddlewaretoken: csrftoken,
        task:id,
        x_pos:position.left,
        y_pos:position.top},
          function(data) { });
}

jsPlumb.bind("ready", function() {
    jsPlumb.Defaults.Containter = $("#workflow_vis");
    jsPlumb.draggable($(".draggable"), {containment:'#workflow_vis', stop:drop_alert});
    jsPlumb.importDefaults({
        anchor: "Continuous",
        connector: ["StateMachine", {curviness:20}],
        connectorStyle: {strokeStyle:"#000", lineWidth:1},
        Endpoint: ["Dot", {radius:2}],
        HoverPaintStyle: {strokeStyle: "#42a62c", lineWidth:2},
        ConnectionOverlays: [ ["Arrow",{ location:1,
                                         id:"arrow",
                                         length:10, foldback: 0.0}]],
        });
    $(".source").each(function(i,e){
        var p = $(e).parent();
        jsPlumb.makeSource($(e), {
            parent:p,
            anchor:"Continuous",
            connector: ["StateMachine", { curviness:20 } ],
            connectorStyle: {strokeStyle:"#000", lineWidth:1},
        });
    });
    jsPlumb.bind("beforeDrop", connections);
    $(".taskNode").each( function(i, e) {
        jsPlumb.makeTarget(jsPlumb.getSelector(e), {
            anchor: "Continuous",
            connector: ["StateMachine", {curviness:20}],
            connectorStyle: {strokeStyle:"#000", lineWidth:1},
                dragOptions: {hoverClass:"dragHover"},});
    });
    //alert(task_edges);
    for (i = 0; i < task_edges.length; ++i) {
        jsPlumb.connect({source:task_edges[i][0],
                         target:task_edges[i][1],
                        anchor: "Continuous",
                            });
    }
});
if (typeof privelege != "undefined"){
    jsPlumb.bind("dblclick", deleteConnection);
}

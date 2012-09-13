function show_user() {
    $("#server").addClass("hidden");
    $("#user").toggleClass("hidden");
}

function show_server() {
    $("#user").addClass("hidden");
    $("#server").toggleClass("hidden");


}


$(document).ready(function () {
    $("#user_but").click(show_user);
    $("#server_but").click(show_server);


});

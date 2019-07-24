$(document).keyup(function(event) {
    if ($("#text").is(":focus") && (event.keyCode == 13)) {
        $("#button").click();
    }
    if ($("#text2").is(":focus") && (event.keyCode == 13)) {
        $("#button2").click();
    }
});
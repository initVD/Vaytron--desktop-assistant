
$(document).ready(function() {

    //display speak message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message li:first").text(message);
        $(".siri-message").textillate('start');
    
    }

    //display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("SiriWave").attr("hidden", true);
    }

    // Optional: Handle text returned from Python if you want to log it
    eel.expose(receiverText)
    function receiverText(message) {
        console.log("Vaytron said: " + message);
        // You can add code here later to append this message to a chat history box
    }

});
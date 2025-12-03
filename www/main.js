$(document).ready(function() {
    $('.text').textillate({
        loop: true, sync: true,
        in: { effect: 'bounceIn' },
        out: { effect: 'bounceOut' },
    });

    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 900, height: 200, style: 'ios9',
        amplitude: "1", speed: "0.30", autostart: true,
    });

    $('.siri-message').textillate({
        loop: true, sync: true,
        in: { effect: 'fadeInUp', sync: true },
        out: { effect: 'fadeInOut', sync: true },
    });

    $('#MicBtn').click(function() {
        eel.playAssistantSound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands();
    });

    function sendTextCommand() {
        var message = $("#chatbox").val();
        if (message.trim() !== "") {
            eel.playAssistantSound();
            $("#chatbox").val("");
            $(".siri-message").text(message);
            eel.chat(message);
            $('#Oval').attr('hidden', false);
            $('#SiriWave').attr('hidden', true);
        }
    }

    $("#chatbox").keypress(function(e) {
        if (e.which == 13) {
            sendTextCommand();
        }
    });

    $("#SendBtn").click(function() {
        sendTextCommand();
    });
});
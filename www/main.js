$(document).ready(function() {

    const video = document.getElementById("startup-video");
    const videoContainer = document.getElementById("video-container");
    const mainInterface = document.getElementById("main-interface");

    if (video) {
        // Start muted to ensure autoplay works
        video.muted = true; 
        video.play().then(() => {
            // Unmute after a small delay
            setTimeout(() => { video.muted = false; }, 500);
        }).catch((error) => {
            $("#start-btn").attr("hidden", false);
            $("#start-btn").click(() => {
                video.muted = false; video.play();
                $("#start-btn").attr("hidden", true);
            });
        });

        video.addEventListener('ended', () => {
            $(videoContainer).fadeOut(1000, function() {
                $(mainInterface).attr("hidden", false);
                $(mainInterface).css("opacity", 1);
                // Trigger Greeting
                eel.chat("Introduce yourself"); 
            });
        });
    }

    $('.text').textillate({ loop: true, sync: true, in: { effect: 'bounceIn' }, out: { effect: 'bounceOut' } });
    $('.siri-message').textillate({ loop: true, sync: true, in: { effect: 'fadeInUp', sync: true }, out: { effect: 'fadeInOut', sync: true } });

    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 900, height: 200, style: 'ios9',
        amplitude: "1", speed: "0.30", autostart: true,
    });

    $('#MicBtn').click(function() {
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands();
    });

    function sendTextCommand() {
        var message = $("#chatbox").val();
        if (message.trim() !== "") {
            $("#chatbox").val("");
            $(".siri-message").text(message);
            eel.chat(message);
            $('#Oval').attr('hidden', false);
            $('#SiriWave').attr('hidden', true);
        }
    }

    $("#chatbox").keypress(function(e) {
        if (e.which == 13) { sendTextCommand(); }
    });

    $("#SendBtn").click(function() { sendTextCommand(); });
});
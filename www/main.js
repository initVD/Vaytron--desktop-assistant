$(document).ready(function() {

    // =========================================================
    // 1. VIDEO STARTUP LOGIC (Prevents Pausing)
    // =========================================================
    const video = document.getElementById("startup-video");
    const videoContainer = document.getElementById("video-container");
    const mainInterface = document.getElementById("main-interface");

    if (video) {
        // Step A: Start muted to trick the browser's autoplay policy
        video.muted = true; 
        
        video.play().then(() => {
            // Step B: Once playing, unmute it after a tiny delay
            setTimeout(() => {
                video.muted = false;
            }, 500);
        }).catch((error) => {
            console.log("Autoplay blocked:", error);
            // Fallback: Show button if the browser is extremely strict
            $("#start-btn").attr("hidden", false);
            $("#start-btn").click(() => {
                video.muted = false;
                video.play();
                $("#start-btn").attr("hidden", true);
            });
        });

        // Step C: When video ends, switch to Jarvis UI
        video.addEventListener('ended', () => {
            $(videoContainer).fadeOut(1000, function() {
                // Reveal the main interface
                $(mainInterface).attr("hidden", false);
                $(mainInterface).css("opacity", 1);
                
                // Optional: Ask Jarvis to introduce himself
                eel.chat("Introduce yourself"); 
            });
        });
    }

    // =========================================================
    // 2. TEXT ANIMATIONS (Textillate)
    // =========================================================
    $('.text').textillate({
        loop: true, sync: true,
        in: { effect: 'bounceIn' },
        out: { effect: 'bounceOut' },
    });

    $('.siri-message').textillate({
        loop: true, sync: true,
        in: { effect: 'fadeInUp', sync: true },
        out: { effect: 'fadeInOut', sync: true },
    });

    // =========================================================
    // 3. SIRI WAVE INITIALIZATION
    // =========================================================
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 900, height: 200, style: 'ios9',
        amplitude: "1", speed: "0.30", autostart: true,
    });

    // =========================================================
    // 4. BUTTON & INPUT HANDLERS
    // =========================================================
    
    // Mic Button Click
    $('#MicBtn').click(function() {
        // eel.playAssistantSound(); // Uncomment if you kept this function in Python
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands();
    });

    // Helper function to send text
    function sendTextCommand() {
        var message = $("#chatbox").val();
        if (message.trim() !== "") {
            // eel.playAssistantSound(); // Uncomment if needed
            $("#chatbox").val("");
            $(".siri-message").text(message);
            eel.chat(message);
            
            // Switch back to Hood mode for text replies
            $('#Oval').attr('hidden', false);
            $('#SiriWave').attr('hidden', true);
        }
    }

    // Handle "Enter" key in chatbox
    $("#chatbox").keypress(function(e) {
        if (e.which == 13) {
            sendTextCommand();
        }
    });

    // Send Button Click
    $("#SendBtn").click(function() {
        sendTextCommand();
    });

});
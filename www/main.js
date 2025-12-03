$(document).ready(function() {
    
    // Textillate animation for the greeting text
    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: 'bounceIn' },
        out: { effect: 'bounceOut' },
    });

    // SiriWave configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 900,
        height: 200,
        style: 'ios9',
        amplitude: "1",
        speed: "0.30",
        autostart: true,
    });

    // Message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: 'fadeInUp', sync: true },
        out: { effect: 'fadeInOut', sync: true },
    });

    // --- NEW: MIC BUTTON CLICK ---
    $('#MicBtn').click(function() {
        eel.playAssistantSound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands()(); // Trigger Python Voice Command
    });

    // --- NEW: KEYBOARD INTERACTION ---
    function sendTextCommand() {
        var message = $("#chatbox").val();
        if (message.trim() !== "") {
            // 1. Play sound
            eel.playAssistantSound();
            
            // 2. Show text on screen immediately
            $("#chatbox").val(""); // Clear input
            $(".siri-message").text(message); // Show what user typed
            
            // 3. Send to Python backend
            eel.chat(message);
            
            // 4. Ensure visuals are correct (Optional: switch to SiriWave briefly or stay on Hood)
            $('#Oval').attr('hidden', false);
            $('#SiriWave').attr('hidden', true);
        }
    }

    // 1. Detect "Enter" key in chatbox
    $("#chatbox").keypress(function(e) {
        if (e.which == 13) {
            sendTextCommand();
        }
    });

    // 2. Detect Send Button Click (Make sure to remove 'hidden' from HTML if you want to see it)
    $("#SendBtn").click(function() {
        sendTextCommand();
    });

});
$(document).ready(function() {
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: 'bounceIn',
        },
        out: {
            effect: 'bounceOut',
        },
    });
    //siri config...
    
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 900,
    height: 200,
    style: 'ios9',
    amplitude: "1",
    speed: "0.30",
    autostart: true,


    
  });

  //siri message animation
   $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: 'fadeInUp',
            sync: true,
        },
        out: {
            effect: 'fadeInOut',
            sync: true,
        },
    });
    //micbtn click event
    $('#MicBtn').click(function() {
        eel.playAssistantSound();
        $('#Oval').attr('hidden', true);
        $('#SiriWave').attr('hidden', false);
        eel.allCommands()() 

    }); 
    $("#chatbox").keypress(function(e){
        if (e.which == 13){
            sendTextCommand();
        }
    })

});
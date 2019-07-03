
var video = document.getElementById('tryButton');
video.addEventListener('click', onClickVideo);

function onClickVideo(event) {
    var target = event.target;
    if (target.tagName !== 'A') return;
    var myDiv = document.createElement('div');
    var myVideo = document.createElement('iframe');
    var gif = document.getElementById('myGifId');

    myDiv.className = "shadowPage";
    myDiv.id = "shadowPagiId";
    myVideo.className = "youTubeVideo"
    myVideo.setAttribute('src', "https://www.youtube.com/embed/tdHqabWGlVE");
    myVideo.id = "youTuveVideoId";
    gif.appendChild(myDiv);
    gif.appendChild(myVideo);
    
    // myDiv.appendChild(myVideo);
    // tryButton.appendChild(myDiv);

    var blackFon = document.getElementById('shadowPagiId');
    blackFon.addEventListener('click', onClickPage);
};

function onClickPage(event) {
    var gif2 = document.getElementById('myGifId');
    var myDiv2 = document.getElementById('shadowPagiId');
    var myVideo2 = document.getElementById('youTuveVideoId');
    
    gif2.removeChild(myVideo2);
    gif2.removeChild(myDiv2);
};
 
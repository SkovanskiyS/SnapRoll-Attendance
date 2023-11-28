'use strict';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById("snap");
const errorMsgElement = document.querySelector('span#errorMsg');


const constraints = {
    audio: false,
    video: {
        width: 1280, height: 720
    }
};

// Access webcam
async function init() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    } catch (e) {
        errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
}

// Success
function handleSuccess(stream) {
    window.stream = stream;
    video.srcObject = stream;
}

var context = canvas.getContext('2d');
var downloadButton = document.getElementById("downloadButton"); // Assuming you have a button with this ID in your HTML

snap.addEventListener("click", function() {
  video.pause()
  var imageWidth = 900;
  var imageHeight = 500;
  var centerX = canvas.width / 2;
  var centerY = canvas.height / 2;
  var x = centerX - imageWidth / 2;
  var y = centerY - imageHeight / 2;

  // Draw the image
  context.drawImage(video, x, y, imageWidth, imageHeight);

    // Convert the canvas content to a data URL 
    var dataURL = canvas.toDataURL('image/png');

    // Create a link for downloading
    downloadButton.href = dataURL;
    downloadButton.download = 'snapshot.png'; // You can customize the file name and extension

    // Simulate a click on the download link to trigger the download
    downloadButton.click();
});

const stopButton = document.getElementById('stopButton');

stopButton.addEventListener('click', stopStream);

// Stop stream
function stopStream() {
    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => {
        track.stop();
    });

    video.srcObject = null;
}

function openCamera(){
      init();
      var div = document.getElementById('hiddenDiv');
      div.style.display = 'block';
}

function closeCamera(){
      stopStream();
      var div = document.getElementById('hiddenDiv');
      div.style.display = 'none';
}

//function closeDivOutside() {
//    var div = document.getElementById('hiddenDiv');
//    console.log(event);
//    div.style.display = 'none';
//
//    const stream = video.srcObject;
//    const tracks = stream.getTracks();
//
//    tracks.forEach(track => {
//        track.stop();
//    });
//
//    video.srcObject = null;
//
//}






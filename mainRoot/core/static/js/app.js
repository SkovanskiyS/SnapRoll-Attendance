'use strict';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById("snap");
const errorMsgElement = document.querySelector('span#errorMsg');
const savePic = document.getElementById("save");
const reg_face_id = document.getElementById("reg_face_id");

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
    var img = document.getElementById("myImage");

    context.drawImage(video, x, y, imageWidth, imageHeight);
    
    var dataURL = canvas.toDataURL('image/png');
    downloadButton.href = dataURL;
//    downloadButton.download = 'image.png';
    console.log(downloadButton);
    //console.log(downloadButton.href);
    //downloadButton.click();
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


function retakePic(){
    video.play();
    var myCheckbox = document.getElementById("defaultCheck2");
    downloadButton.href = 'none';
    myCheckbox.checked = false;

    // var div = document.getElementById('hiddenDiv');
    // div.style.display = 'none';
}

// savePic.addEventListener('click',savePic);

function savePicFunc(){
    var myCheckbox = document.getElementById("defaultCheck2");
    var image_data_input = document.getElementById("imageDataInput");
    var div = document.getElementById('hiddenDiv');
    let data_url = downloadButton.href;
    if (data_url.includes('none') || data_url=='') {
        alert('Please, take a shoot of your face!');
    }
    else{
        alert('Successfully saved!');
        div.style.display = 'none';
        myCheckbox.checked = true;
        image_data_input.value = data_url;
        console.log(data_url);
        stopStream();
        
    }

}

function checkValidData(){

    if(myCheckbox.checked) {
        return false;
    }
    else{
        alert("Please, register your face!");
        return false;
    }

        var myCheckbox = document.getElementById("defaultCheck2");

    var fileInput = document.getElementById('formFile');

    // Get the selected file
    var selectedFile = fileInput.files[0];

    // Update the input element's name attribute
    if (selectedFile) {
        console.log('he')
        fileInput.name = "File name";
    } else {
        // If no file is selected, you may want to reset the name to its default value
        fileInput.name = 'face';
    }
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






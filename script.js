var button = document.getElementById('button');

button.onclick = function() {
    var div = document.getElementById('newpost');
    if (div.style.display !== 'none') {
        div.style.display = 'none';
    }
    else {
        div.style.display = 'block';
    }
};

function resizeToMax(id){
    myImage = new Image() 
    var img = document.getElementById(id);
    myImage.src = img.src; 
    if(myImage.width / document.body.clientWidth > myImage.height / document.body.clientHeight){
        img.style.width = "100%";
    } else {
        img.style.height = "100%";
    }
}


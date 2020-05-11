// Get the modal
var modal = document.getElementById("map_modal");
var modal1 = document.getElementById("map_modal1");
var modal2 = document.getElementById("map_modal2");
var modal3 = document.getElementById("map_modal3");
var btn1 = document.getElementById("popup_btn1");
var btn2 = document.getElementById("popup_btn2");
var btn3 = document.getElementById("popup_btn3");
var btnLeft2 = document.getElementById("popup_btn2_left");
var btnLeft3 = document.getElementById("popup_btn3_left");

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];

document.addEventListener("DOMContentLoaded", function(event) {
    modal.style.display = "block";
    modal1.style.display = "block";
    // modal2.style.display = "block";
    // modal3.style.display = "block";
});

btn1.onclick = function() {
    modal1.style.display = "none";
    modal2.style.display = "block";
}

btn2.onclick = function() {
    modal2.style.display = "none";
    modal3.style.display = "block";
}

btn3.onclick = function() {
    modal3.style.display = "none";
    modal.style.display = "none";
}

btnLeft2.onclick = function() {
    modal2.style.display = "none";
    modal1.style.display = "block";
}

btnLeft3.onclick = function() {
    modal3.style.display = "none";
    modal2.style.display = "block";
}



// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }

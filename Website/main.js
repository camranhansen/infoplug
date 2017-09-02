/* Set the width of the side navigation to 45% */
function openNav() {
    document.getElementById("mySidenav").style.width = "45%";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}


function updateDate(){
    
    document.getElementById("date").innerHTML =  Date("03/25/2015");
    
    
}
updateDate();


function addDevice(){
    
    setTimeout(function () {
       window.location.href = "addDevice.htm"; 
    }, 600);
    
}

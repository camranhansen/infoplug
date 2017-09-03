/* Set the width of the side navigation to 250px */
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
       window.location.href = "/static/addDevice.html"; //will redirect to your blog page (an ex: blog.html)
    }, 600);
    
}

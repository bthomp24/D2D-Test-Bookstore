function openPage(pageName, elmnt) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
    }
    document.getElementById(pageName).style.display = "block";
    elmnt.style.backgroundColor = "#333";

    
}

// Get the element with id="defaultOpen" and click on it
function start() {
    document.getElementById("defaultOpen").click();

    window.onscroll = function () { myFunction() };

    var navbar = document.getElementById("navbar");
    var sticky = navbar.offsetTop;

    function myFunction() {
        if (window.pageYOffset >= sticky) {
            navbar.classList.add("sticky")
        } else {
            navbar.classList.remove("sticky");
        }
    }


}

function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

function revealQForm() {
    if (document.getElementById('query_form').style.display == 'none'){
        document.getElementById('query_form').style.display = 'block'
        document.querySelector('#queryFormBtn').textContent = 'Hide Form'
        document.getElementById("query_form").scrollIntoView();
    }
    else {
        document.getElementById('query_form').style.display = 'none'
        document.querySelector('#queryFormBtn').textContent = 'Search Historical Records'
    }
}
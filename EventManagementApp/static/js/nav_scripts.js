const body = document.querySelector("nav_body"),
    nav = document.querySelector("nav"),
    searchToggle = document.querySelector(".searchToggle"),
    sidebarOpen = document.querySelector(".sidebarOpen"),
    siderbarClose = document.querySelector(".siderbarClose");


searchToggle.addEventListener("click", () => {
    searchToggle.classList.toggle("active");
});


sidebarOpen.addEventListener("click", () => {
    nav.classList.add("active");
});

body.addEventListener("click", e => {
    let clickedElm = e.target;
    if (!clickedElm.classList.contains("sidebarOpen") && !clickedElm.classList.contains("siderbarClose")) {
        nav.classList.remove("active");
    }
});
function close_button_function(el) {
    //const el = event.target;
    let parent = el.parentNode;

    while (!(parent.classList.contains("show"))){
        parent = parent.parentNode;
    }
    parent.classList.remove("show");
}
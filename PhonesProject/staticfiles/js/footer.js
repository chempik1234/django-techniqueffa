function footerf() {
    const footer = document.getElementsByTagName('footer')[0];
    const susick = document.getElementById('main-container');

    const windowHeight = window.innerHeight;
    let footerBottom = footer.getBoundingClientRect().bottom;

    while (footerBottom < windowHeight) {
        footer.style.marginTop = `${windowHeight - footerBottom}px`;
        footerBottom = footer.getBoundingClientRect().bottom;
        console.log(footerBottom);
    }
}

window.addEventListener('load', footerf);
window.addEventListener('resize', footerf);
function footerf() {
    const
        footer = document.getElementsByTagName('footer')[0],
        susick = document.getElementById('main-nav');
    footer.style.marginTop = susick.clientHeight-footer.clientHeight + 30 + 'px';
}

window.addEventListener('load', footerf);
window.addEventListener('resize', footerf);
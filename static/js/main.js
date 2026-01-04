function openModal(id) {
    document.getElementById(id).classList.add('open');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('open');
}

// Close modal if clicked outside of content
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('open');
    }
}

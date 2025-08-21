const modalPreloader = document.querySelector('#modal-preloader');
if (modalPreloader) {
  window.addEventListener('load', () => {
    modalPreloader.remove();
  });
}
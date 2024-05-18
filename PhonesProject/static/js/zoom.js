const zoomContainer = document.querySelector('.image-zoom-container');
const image = document.querySelector('.main-image');
const zoomFactor = 1.5;

zoomContainer.addEventListener('mousemove', (e) => {
  const containerRect = zoomContainer.getBoundingClientRect();
  const imageRect = image.getBoundingClientRect();

  const mouseX = e.clientX - containerRect.left;
  const mouseY = e.clientY - containerRect.top;

  const offsetX = (0.5 - mouseX / containerRect.width) * (imageRect.width - containerRect.width) * zoomFactor;
  const offsetY = (0.5 - mouseY / containerRect.height) * (imageRect.height - containerRect.height) * zoomFactor;

  image.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${zoomFactor})`;
});

zoomContainer.addEventListener('mouseleave', () => {
  image.style.transform = 'translate(0, 0)';
});
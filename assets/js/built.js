document.addEventListener('DOMContentLoaded', function () {
  const container = document.getElementById('dragContainer');
  let isDown = false;
  let startX;
  let scrollLeft;

  // Khi nhấn chuột xuống
  container.addEventListener('mousedown', (e) => {
    isDown = true;
    container.classList.add('active');
    startX = e.pageX - container.offsetLeft;
    scrollLeft = container.scrollLeft;
    // Ngăn quán tính mặc định
    e.preventDefault();
  });

  // Khi thả chuột
  container.addEventListener('mouseup', () => {
    isDown = false;
    container.classList.remove('active');
  });

  // Khi chuột rời khỏi container
  container.addEventListener('mouseleave', () => {
    isDown = false;
    container.classList.remove('active');
  });

  // Khi kéo chuột
  container.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - container.offsetLeft;
    const walk = (x - startX); // Điều chỉnh tốc độ kéo (bỏ nhân 2 để mượt hơn)
    container.scrollLeft = scrollLeft - walk;
  });

  // Hỗ trợ kéo trên thiết bị cảm ứng
  container.addEventListener('touchstart', (e) => {
    isDown = true;
    startX = e.touches[0].pageX - container.offsetLeft;
    scrollLeft = container.scrollLeft;
    e.preventDefault();
  });

  container.addEventListener('touchend', () => {
    isDown = false;
  });

  container.addEventListener('touchmove', (e) => {
    if (!isDown) return;
    const x = e.touches[0].pageX - container.offsetLeft;
    const walk = (x - startX);
    container.scrollLeft = scrollLeft - walk;
    e.preventDefault();
  });
});
const menuToggle = document.querySelector('.menuToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const closeBtn = document.querySelector('.close_btn');
    const navbarCollapse = document.querySelector('#navbarNav');

    const openMenu = function() {
        menuToggle.style.display = 'none'; 
        overlay.style.display = 'block';
        setTimeout(function() {
            overlay.classList.add('show');
        }, 10);
        
        sidebar.classList.add('show');
        
        // Ẩn navbar-collapse khi mở menu
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
        navbarCollapse.style.display = 'none';
        
        document.body.style.overflow = 'hidden';
    };
    
    const closeMenu = function() {
        overlay.classList.remove('show');
        menuToggle.style.display = 'block';
        setTimeout(function() {
            overlay.style.display = 'none';
        }, 300);
        
        sidebar.classList.remove('show');
        
        // Đảm bảo navbar-collapse ẩn và khôi phục trạng thái
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
        navbarCollapse.style.display = 'none';
        document.querySelector('.navbar').style.overflowX = 'hidden';
        
        document.body.style.overflow = 'auto';
    };
    
    menuToggle.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);   

document.addEventListener('DOMContentLoaded', () => {
  // Hàm khởi tạo carousel
  function initializeCarousel(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const wrapper = container.querySelector('.items-wrapper');
    let isDragging = false;
    let startX = 0;
    let scrollLeft = 0;
    
    function adjustImageSize() {
      const items = wrapper.querySelectorAll('.item');
      const containerWidth = container.offsetWidth;
      let visibleItems = 5;
      
      if (window.innerWidth < 576) visibleItems = 1;
      else if (window.innerWidth < 768) visibleItems = 2;
      else if (window.innerWidth < 992) visibleItems = 3;
      else if (window.innerWidth < 1200) visibleItems = 4;
      
      const padding = 20;
      const itemWidth = (containerWidth - (padding * (visibleItems - 1))) / visibleItems;
      
      items.forEach(item => {
        const img = item.querySelector('img');
        img.style.maxWidth = `${itemWidth}px`;
        img.style.width = '100%';
        item.style.flex = `0 0 ${itemWidth}px`;
        item.style.padding = `0 ${padding/2}px`;
        img.draggable = false;
        img.addEventListener('dragstart', (e) => e.preventDefault());
      });
      
      wrapper.style.width = `${items.length * (itemWidth + padding)}px`;
    }
    
    function snapToEdge() {
      const items = wrapper.querySelectorAll('.item');
      if (!items.length) return;
      
      const itemWidth = items[0].offsetWidth;
      const index = Math.round(container.scrollLeft / itemWidth);
      container.scrollTo({
        left: index * itemWidth,
        behavior: 'smooth'
      });
    }
    
    adjustImageSize();
    
    container.addEventListener('dragstart', (e) => e.preventDefault());
    container.addEventListener('drop', (e) => e.preventDefault());
    container.onselectstart = () => false;
    
    container.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.pageX - container.offsetLeft;
      scrollLeft = container.scrollLeft;
      container.style.cursor = 'grabbing';
      e.preventDefault(); 
    });
    
    container.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      e.preventDefault();
      const x = e.pageX - container.offsetLeft;
      const walk = (x - startX) * 1.5; 
      container.scrollLeft = scrollLeft - walk;
    });
    
    document.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        container.style.cursor = 'grab';
        snapToEdge();
      }
    });
    
    container.addEventListener('mouseleave', () => {
      if (isDragging) {
        isDragging = false;
        container.style.cursor = 'grab';
        snapToEdge();
      }
    });
    
    container.addEventListener('touchstart', (e) => {
      isDragging = true;
      startX = e.touches[0].pageX - container.offsetLeft;
      scrollLeft = container.scrollLeft;
      e.preventDefault(); 
    }, { passive: false });
    
    container.addEventListener('touchmove', (e) => {
      if (!isDragging) return;
      const x = e.touches[0].pageX - container.offsetLeft;
      const walk = (x - startX) * 1.5;
      container.scrollLeft = scrollLeft - walk;
      e.preventDefault(); 
    }, { passive: false });
    
    container.addEventListener('touchend', () => {
      isDragging = false;
      snapToEdge();
    });
    
    return adjustImageSize; // Trả về hàm adjustImageSize để sử dụng với resize
  }
  
  // Khởi tạo carousel đầu tiên
  const adjustImageSize1 = initializeCarousel('dragContainer');
  
  // Khởi tạo carousel thứ hai
  const adjustImageSize2 = initializeCarousel('dragContainer-2');
  
  // Xử lý sự kiện resize cho cả hai carousel
  window.addEventListener('resize', () => {
    if (adjustImageSize1) adjustImageSize1();
    if (adjustImageSize2) adjustImageSize2();
  });
});

// Hàm cuộn carousel theo id
function scrollContainer(amount, containerId) {
  const container = document.getElementById(containerId || 'dragContainer');
  if (container) {
    container.scrollBy({
      left: amount,
      behavior: 'smooth'
    });
  }
}
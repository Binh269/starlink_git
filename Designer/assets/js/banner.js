const firstNav = document.querySelector('nav.navbar.fixed-top'); 
const secondNav = document.querySelector('nav.navbar:not(.fixed-top)'); 
const firstNavContent = firstNav.innerHTML;
const secondNavContent = secondNav.innerHTML;
window.addEventListener('scroll', () => {
  const secondNavPosition = secondNav.getBoundingClientRect().top + window.scrollY;
  const scrollPosition = window.scrollY;
  const colorThreshold = 50;
  if (scrollPosition >= secondNavPosition) {
    firstNav.innerHTML = secondNavContent;
    firstNav.style.backgroundColor = '#303030'; 
  } else {
    firstNav.innerHTML = firstNavContent;
    if (scrollPosition > colorThreshold) {
      firstNav.style.backgroundColor = 'rgb(59 57 61)'; 
    } else {
      firstNav.style.backgroundColor = 'transparent'; 
    }
  }
});

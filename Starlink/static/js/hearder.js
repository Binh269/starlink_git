const navbar = document.querySelector('nav.navbar');
window.addEventListener('scroll', () => {
  const scrollPosition = window.scrollY;
  const threshold = 500;
  if (scrollPosition > threshold) {
    navbar.style.backgroundColor = 'rgb(59 57 61)'; 
  } else {
    navbar.style.backgroundColor = 'transparent'; 
  }
});


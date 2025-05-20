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
document.querySelector('.fixed_site').addEventListener('click', function() {
    window.location.href = 'business_fixed-site.html';
});

document.querySelector('.mobility').addEventListener('click', function() {
    window.location.href = 'business_mobility.html';
});

document.querySelector('.maritime').addEventListener('click', function() {
    window.location.href = 'business_maritime.html';
});

document.querySelector('.direct_to_cell').addEventListener('click', function() {
    window.location.href = 'business_direct-to-cell.html';
});



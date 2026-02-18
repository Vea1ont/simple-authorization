const carousel = document.querySelectorAll('.carousel');

carousel.forEach(carousel => {
  const slides = carousel.querySelectorAll('.slide');
  const indicatorsContainer = carousel.querySelector('.carousel-indicators');

  slides.forEach((slide, index) => {
    const indicator = document.createElement('div');

    indicator.classList.add('indicator');

    if (index === 0) {
      indicator.classList.add('active');
    }

    indicatorsContainer.appendChild(indicator);
  });

  const indicators = carousel.querySelectorAll('.indicator');

  let currentIndex = 0;
  let autoSlideInterval;
  let pauseTimeout;


  function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    slides[index].classList.add('active');
    indicators[index].classList.add('active');
    console.log
  }

  showSlide(currentIndex);

  function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % slides.length;
      showSlide(currentIndex);
    }, 5000);
  }

  function stopAutoSlide() {
    clearInterval(autoSlideInterval);
  };

  function autoSlideAfterDelay() {
    if (pauseTimeout) {
      clearTimeout(pauseTimeout);
    }
    
    stopAutoSlide();
    
    pauseTimeout = setTimeout(() => {
      startAutoSlide();
    }, 15000);
  }

  startAutoSlide();

  carousel.addEventListener('click', (e) => {
    stopAutoSlide(); 
    const rect = carousel.getBoundingClientRect();
    const clickPosition = e.clientX - rect.left;
    
    
    if (clickPosition < rect.width / 2) {
      currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    } else {
      currentIndex = (currentIndex + 1) % slides.length;
    }
    showSlide(currentIndex);
    autoSlideAfterDelay();
  });


})








window.addEventListener('scroll', function () {
    var header = document.querySelector('header');
    if (window.scrollY > 0) {
      header.classList.add('shadow'); // Add shadow when not at the top
    } else {
        header.classList.remove('shadow'); // Add shadow when not at the top
    }
});
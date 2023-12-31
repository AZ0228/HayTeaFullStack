window.addEventListener('scroll', function () {
    var header = document.querySelector('header');
    if (window.scrollY > 0) {
      header.classList.add('shadow'); // Add shadow when not at the top
    } else {
        header.classList.remove('shadow'); // Add shadow when not at the top
    }
});

document.addEventListener("DOMContentLoaded", function() {
  const container = document.querySelector("#favorites-container");
  const middleScrollPosition = container.scrollWidth / 2 - container.clientWidth / 2;
  container.scrollLeft = middleScrollPosition;
});
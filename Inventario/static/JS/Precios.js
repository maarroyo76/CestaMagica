window.onload = function() {
    const priceElements = document.querySelectorAll('.price');
    Array.prototype.forEach.call(priceElements, function(element) {
      const price = parseFloat(element.getAttribute('data-raw-price'));
      if (!isNaN(price)) {
        element.textContent = price.toLocaleString('es-CL', { style: 'currency', currency: 'CLP' });
      }
    });
}
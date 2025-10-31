/**
 * @param {object} options
 * @param {string} options.message
 * @param {string} [options.type="success"]
 */
function showToast({message, type = "success"}) {
  const toast = document.createElement("div");
  toast.className = `custom-toast ${type}`;

  const iconMap = {
    success: "✔️",
    danger: "❌",
    info: "ℹ️",
    warning: "⚠️"
  };

  toast.innerHTML = `<span>${iconMap[type] || "🔔"}</span> ${message}`;

  const container = document.getElementById("custom-toast-container");

  if (container) {
    container.appendChild(toast);
  } else {
          const tempContainer = document.createElement("div");
          tempContainer.id = "custom-toast-container";
          tempContainer.style = "position: fixed; bottom: 5rem; right: 1.5rem; z-index: 9999;";
          document.body.appendChild(tempContainer);
          tempContainer.appendChild(toast);
     }

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

/**
 * @param {number} count - El número total de ítems.
 */
function updateCartBadge(count) {
  if (count > 0) {
    $("#navbar-cart-count").text(count).fadeIn();
  } else {
    $("#navbar-cart-count").fadeOut();
  }
}



$(document).ready(function() {
    
    const searchInput = $('#navbar-search-input');
    const resultsContainer = $('#navbar-search-results');
    let debounceTimer; // Variable para el "debounce"

    searchInput.on('keyup', function() {
        const searchTerm = $(this).val();

        // Limpiamos el timer anterior
        clearTimeout(debounceTimer);

        if (searchTerm.length < 2) {
            // Si la búsqueda es muy corta, no buscamos y ocultamos resultados
            resultsContainer.empty().hide();
            return;
        }

        // --- Pro Tip: Debouncing ---
        // Esto evita enviar un request por CADA tecla.
        // Espera 300ms después de que el usuario DEJE de teclear.
        debounceTimer = setTimeout(function() {
            // Hacemos la llamada AJAX
            $.ajax({
                url: '/search-autocomplete/', // La URL que creamos
                data: {
                    'term': searchTerm
                },
                dataType: 'json',
                success: function(data) {
                    // 1. Limpiamos resultados anteriores
                    resultsContainer.empty();

                    // 2. Revisamos si hay resultados
                    if (data.length > 0) {
                        // 3. Creamos el HTML para cada resultado
                        data.forEach(function(producto) {
                            const resultHtml = `
                                <a href="${producto.url}" class="list-group-item list-group-item-action d-flex align-items-center     justify-content-between">
                                    <div class="d-flex align-items-center">
                                        <img src="${producto.imagen}" alt="${producto.nombre}" style="width: 40px; height: 40px; object-fit: contain; margin-right: 10px;">
                                        <span>${producto.nombre}</span>
                                    </div>
                                    <strong style="color: #477c3b;">
                                        $${producto.precio.toLocaleString('es-CL')}
                                    </strong>
                                </a>
                            `;
                            resultsContainer.append(resultHtml);
                        });
                        // 4. Mostramos el contenedor
                        resultsContainer.show();
                    } else {
                        // Opcional: mostrar un mensaje de "no se encontró"
                        resultsContainer.append('<span class="list-group-item">No se encontraron productos.</span>').show();
                    }
                }
            });
        }, 100); //
    });

    // Ocultar resultados si el usuario hace clic fuera
    $(document).on('click', function(e) {
        if (!$(e.target).closest('#navbar-search-input').length) {
            resultsContainer.empty().hide();
        }
    });
});
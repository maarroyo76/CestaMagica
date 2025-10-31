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
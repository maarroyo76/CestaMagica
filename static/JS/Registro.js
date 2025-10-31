document.addEventListener("DOMContentLoaded", () => {
        const form = document.getElementById("form_registro");
        const pass = document.getElementById("pass");
        const confirm_pass = document.getElementById("confirm_pass");

        form.addEventListener("submit", (event) => {
            checkPassword();

            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add("was-validated");
        });

        confirm_pass.addEventListener("input", checkPassword);

        function checkPassword() {
            if (pass.value !== confirm_pass.value) {
                confirm_pass.setCustomValidity("Las contraseñas no coinciden");
            } else {
                confirm_pass.setCustomValidity("");
            }
        }
    });
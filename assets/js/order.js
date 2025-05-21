document.addEventListener("DOMContentLoaded", function () {
            const orderBtn = document.getElementById("order");
            const noidungOrder = document.getElementById("noidung_order");
            const icon = document.getElementById("order-icon");

            orderBtn.addEventListener("click", function () {
                const isVisible = noidungOrder.classList.toggle("show");

                if (isVisible) {
                    icon.classList.remove("fa-chevron-down");
                    icon.classList.add("fa-chevron-up");
                    noidungOrder.style.display = "block";

                } else {
                    icon.classList.remove("fa-chevron-up");
                    icon.classList.add("fa-chevron-down");
                    noidungOrder.style.display = "none";
                }
            });
        });
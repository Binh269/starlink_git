document.addEventListener("DOMContentLoaded", function() {
    function setupDropdown(btnId, listId) {
        const btn = document.getElementById(btnId);
        const list = document.getElementById(listId);

        if (!btn || !list) return;

        btn.addEventListener("click", function(e) {
            e.preventDefault();
            e.stopPropagation();
            list.style.display = list.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function(e) {
            if (!btn.contains(e.target) && !list.contains(e.target)) {
                list.style.display = "none";
            }
        });

        const items = list.querySelectorAll(".dropdown-item");
        items.forEach(item => {
            item.addEventListener("click", function(e) {
                e.preventDefault();
                btn.textContent = this.textContent.trim();
                list.style.display = "none";
            });
        });
    }

    setupDropdown("list_qg", "list-nd-qg");
    setupDropdown("list_tinh", "list-nd-tinh");

    const btn_kdc = document.getElementById("btn_kdc");
    const learn_more_kdc = document.getElementById("learn-more_kdc");
    const noidung_kdc = document.getElementById("noidung_kdc");

    const btn_cv = document.getElementById("btn_cv"); 
    const learn_more_cv = document.getElementById("learn-more_cv");
    const noidung_cv = document.getElementById("noidung_cv");

    btn_kdc.addEventListener("click", function(e) {
        e.preventDefault();
        btn_kdc.style.display = "none";
        learn_more_kdc.style.display = "none";
        noidung_kdc.style.display = "flex";
        btn_cv.style.display = "block";
        learn_more_cv.style.display = "block";
        noidung_cv.style.display = "none";
    });

    btn_cv.addEventListener("click", function(e) {
        e.preventDefault();
        btn_cv.style.display = "none";
        learn_more_cv.style.display = "none";
        noidung_cv.style.display = "flex";
        btn_kdc.style.display = "block";
        learn_more_kdc.style.display = "block";
        noidung_kdc.style.display = "none";
    });
    
  
   const orderBtn = document.getElementById("order");
        const noidungOrder = document.getElementById("noidung_order");
        const icon = document.getElementById("order-icon");

        orderBtn.addEventListener("click", function () {
            const isHidden = noidungOrder.classList.contains("hidden");

            noidungOrder.classList.toggle("hidden");

            // Đổi icon
            if (isHidden) {
                icon.classList.remove("fa-chevron-down");
                icon.classList.add("fa-chevron-up");
            } else {
                icon.classList.remove("fa-chevron-up");
                icon.classList.add("fa-chevron-down");
            }
        });
});

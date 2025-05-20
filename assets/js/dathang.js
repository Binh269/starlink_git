document.addEventListener("DOMContentLoaded", function() {
    const list_qg = document.getElementById("list_qg");
    const list_nd_qg = document.getElementById("list-nd-qg");
  
  
    const btn_kdc = document.getElementById("btn_kdc");
    const learn_more_kdc = document.getElementById("learn-more_kdc");
    const noidung_kdc = document.getElementById("noidung_kdc");

  
    const btn_cv =   document.getElementById("btn_cv"); 
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
  
    list_qg.addEventListener("click", function(e) {
        e.preventDefault();
      e.stopPropagation(); 
        list_nd_qg.style.display = list_nd_qg.style.display === "block" ? "none" : "block";
    });

    document.addEventListener("click", function(e) {
        if (!list_qg.contains(e.target) && !list_nd_qg.contains(e.target)) {
            list_nd_qg.style.display = "none";
        }
    });

    
});
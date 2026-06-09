(function () {
  function initYouTubeFacades() {
    document.querySelectorAll(".youtube-facade").forEach(function (el) {
      if (el.dataset.bound) return;
      el.dataset.bound = "1";
      el.addEventListener("click", function () {
        var id = el.getAttribute("data-id");
        if (!id) return;
        var iframe = document.createElement("iframe");
        iframe.setAttribute("src", "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1");
        iframe.setAttribute("title", "YouTube video");
        iframe.setAttribute("frameborder", "0");
        iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
        iframe.setAttribute("allowfullscreen", "");
        iframe.className = "youtube-iframe";
        el.innerHTML = "";
        el.appendChild(iframe);
        el.classList.add("is-playing");
      });
    });
  }

  function deferArticleMedia(articleId) {
    var article = document.getElementById(articleId);
    if (!article || article.dataset.mediaReady) return;
    article.dataset.mediaReady = "1";
    article.querySelectorAll("img[data-src]").forEach(function (img) {
      img.src = img.getAttribute("data-src");
      img.removeAttribute("data-src");
    });
    initYouTubeFacades();
  }

  window.dwikitDeferArticleMedia = deferArticleMedia;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initYouTubeFacades);
  } else {
    initYouTubeFacades();
  }
})();
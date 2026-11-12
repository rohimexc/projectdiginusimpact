/**
 * Validasi client-side terpadu untuk seluruh input upload file (layer JS).
 * Selalu berjalan berdampingan dengan validasi layer Model dan View/Form di backend.
 */
(function () {
  "use strict";

  var RULES = {
    image: {
      label: "Gambar",
      extensions: [".jpg", ".jpeg", ".png", ".webp"],
      mimePrefixes: ["image/jpeg", "image/png", "image/webp"],
      maxMb: 10,
    },
    video: {
      label: "Video",
      extensions: [".mp4", ".webm", ".ogg"],
      mimePrefixes: ["video/mp4", "video/webm", "video/ogg"],
      maxMb: 100,
    },
    pdf: {
      label: "Dokumen PDF",
      extensions: [".pdf"],
      mimePrefixes: ["application/pdf"],
      maxMb: 20,
    },
    document: {
      label: "Dokumen",
      extensions: [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"],
      mimePrefixes: [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      ],
      maxMb: 25,
    },
  };

  var BLOCKED_MIME_TYPES = [
    "text/html",
    "text/javascript",
    "application/javascript",
    "application/x-javascript",
    "application/x-msdownload",
    "application/x-executable",
    "application/x-php",
    "text/x-php",
    "application/x-python-code",
    "text/x-python",
    "application/x-sh",
    "image/svg+xml",
  ];

  function inferRuleKey(input) {
    var explicit = (input.getAttribute("data-upload-type") || "").toLowerCase().trim();
    if (explicit && RULES[explicit]) {
      return explicit;
    }
    var name = (input.getAttribute("name") || "").toLowerCase();
    if (name === "video_file") return "video";
    if (name === "file_dokumen" || name === "file_utama") return "document";
    if (name === "foto" || name === "gambar") return "image";
    return null;
  }

  function showValidationError(message) {
    if (typeof Swal !== "undefined" && typeof Swal.fire === "function") {
      Swal.fire({
        icon: "error",
        title: "File Tidak Valid",
        text: message,
        confirmButtonColor: "#0b7285",
      });
    } else {
      window.alert(message);
    }
  }

  function getFileExtension(filename) {
    var idx = filename.lastIndexOf(".");
    return idx >= 0 ? filename.slice(idx).toLowerCase() : "";
  }

  function validateFileInput(input, showAlert) {
    var ruleKey = inferRuleKey(input);
    if (!ruleKey || !input.files || input.files.length === 0) {
      return true;
    }

    var rule = RULES[ruleKey];
    var maxMb = parseFloat(input.getAttribute("data-max-mb")) || rule.maxMb;
    var maxBytes = maxMb * 1024 * 1024;
    var file = input.files[0];
    var ext = getFileExtension(file.name || "");
    var mime = (file.type || "").toLowerCase().trim();

    if (!rule.extensions.includes(ext)) {
      var extMsg =
        "Format " +
        rule.label.toLowerCase() +
        " tidak diizinkan (" +
        (ext || "tanpa ekstensi") +
        "). Gunakan: " +
        rule.extensions.join(", ") +
        ".";
      input.value = "";
      if (showAlert) showValidationError(extMsg);
      return false;
    }

    if (mime && BLOCKED_MIME_TYPES.includes(mime)) {
      var dangerousMsg = "Tipe MIME file (" + mime + ") diblokir demi keamanan.";
      input.value = "";
      if (showAlert) showValidationError(dangerousMsg);
      return false;
    }

    if (mime && !rule.mimePrefixes.includes(mime)) {
      var mimeMsg =
        "Tipe konten file (" +
        mime +
        ") tidak sesuai dengan format " +
        rule.label.toLowerCase() +
        " yang diizinkan.";
      input.value = "";
      if (showAlert) showValidationError(mimeMsg);
      return false;
    }

    if (file.size === 0) {
      var emptyMsg = "File yang dipilih kosong (0 byte).";
      input.value = "";
      if (showAlert) showValidationError(emptyMsg);
      return false;
    }

    if (file.size > maxBytes) {
      var actualMb = (file.size / (1024 * 1024)).toFixed(1);
      var sizeMsg =
        "Ukuran file terlalu besar (" +
        actualMb +
        " MB). Maksimal " +
        maxMb +
        " MB untuk " +
        rule.label.toLowerCase() +
        ".";
      input.value = "";
      if (showAlert) showValidationError(sizeMsg);
      return false;
    }

    return true;
  }

  function applyAcceptDefaults(input) {
    var ruleKey = inferRuleKey(input);
    if (!ruleKey) return;
    var rule = RULES[ruleKey];
    if (!input.getAttribute("accept")) {
      input.setAttribute("accept", rule.extensions.join(","));
    }
    if (!input.getAttribute("data-upload-type")) {
      input.setAttribute("data-upload-type", ruleKey);
    }
    if (!input.getAttribute("data-max-mb")) {
      input.setAttribute("data-max-mb", String(rule.maxMb));
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var fileInputs = document.querySelectorAll('input[type="file"]');
    var forms = new Set();

    fileInputs.forEach(function (input) {
      applyAcceptDefaults(input);
      input.addEventListener("change", function () {
        validateFileInput(input, true);
      });
      if (input.form) {
        forms.add(input.form);
      }
    });

    forms.forEach(function (form) {
      form.addEventListener("submit", function (event) {
        var inputs = form.querySelectorAll('input[type="file"]');
        for (var i = 0; i < inputs.length; i++) {
          if (!validateFileInput(inputs[i], true)) {
            event.preventDefault();
            return false;
          }
        }
        return true;
      });
    });
  });
})();


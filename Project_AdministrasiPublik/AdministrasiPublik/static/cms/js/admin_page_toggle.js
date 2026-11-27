// admin_page_toggle.js
document.addEventListener("DOMContentLoaded", function () {
    const contentTypeSelect = document.getElementById("id_content_type");
    if (!contentTypeSelect) return;

    const rowHtml = document.querySelector(".field-html_content");
    const rowFile = document.querySelector(".field-file");
    const rowExtUrl = document.querySelector(".field-external_url");
    const rowIntUrl = document.querySelector(".field-internal_url");

    function updateFields() {
        const val = contentTypeSelect.value;

        // Reset display
        if (rowHtml) rowHtml.style.display = "none";
        if (rowFile) rowFile.style.display = "none";
        if (rowExtUrl) rowExtUrl.style.display = "none";
        if (rowIntUrl) rowIntUrl.style.display = "none";

        if (val === "html") {
            if (rowHtml) rowHtml.style.display = "";
        } else if (val === "pdf" || val === "file_download") {
            if (rowFile) rowFile.style.display = "";
        } else if (val === "external_link") {
            if (rowExtUrl) rowExtUrl.style.display = "";
        } else if (val === "internal_link") {
            if (rowIntUrl) rowIntUrl.style.display = "";
        }
    }

    contentTypeSelect.addEventListener("change", updateFields);
    updateFields();
});

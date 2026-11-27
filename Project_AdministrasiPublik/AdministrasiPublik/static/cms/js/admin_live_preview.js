// admin_live_preview.js
document.addEventListener("DOMContentLoaded", function () {
    const inputs = [
        { id: "id_favicon", previewClass: "field-preview_favicon" },
        { id: "id_header_logo", previewClass: "field-preview_header_logo" },
        { id: "id_footer_logo", previewClass: "field-preview_footer_logo" }
    ];

    inputs.forEach(item => {
        const inputElem = document.getElementById(item.id);
        const container = document.querySelector("." + item.previewClass + " .readonly");

        if (inputElem && container) {
            inputElem.addEventListener("change", function () {
                if (this.files && this.files[0]) {
                    const file = this.files[0];

                    // Validasi ukuran live
                    const isFavicon = item.id.includes("favicon");
                    const maxBytes = isFavicon ? 500 * 1024 : 2 * 1024 * 1024;
                    if (file.size > maxBytes) {
                        alert(`Peringatan: Ukuran file (${(file.size / 1024).toFixed(1)} KB) melebihi batas yang disarankan (${isFavicon ? '500 KB' : '2 MB'})!`);
                    }

                    const objectUrl = URL.createObjectURL(file);
                    container.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                            <img src="${objectUrl}" style="max-height: 50px; max-width: 120px; border: 2px dashed #0f766e; border-radius: 6px; padding: 4px; background: #f8fafc;" />
                            <span style="font-size: 11px; color: #047857; font-weight: bold;">(Preview Baru: ${file.name} - ${(file.size / 1024).toFixed(1)} KB)</span>
                        </div>
                    `;
                }
            });
        }
    });
});

/* Dynamic Form Fields based on Content Type in Django Admin */
document.addEventListener('DOMContentLoaded', function() {
    const contentTypeSelect = document.getElementById('id_content_type');
    if (!contentTypeSelect) return;

    const rowHtml = document.querySelector('.form-row.field-html_content') || document.querySelector('.field-html_content');
    const rowPdf = document.querySelector('.form-row.field-pdf_file') || document.querySelector('.field-pdf_file');
    const rowExternal = document.querySelector('.form-row.field-external_url') || document.querySelector('.field-external_url');
    const rowInternal = document.querySelector('.form-row.field-internal_url') || document.querySelector('.field-internal_url');
    const rowDownload = document.querySelector('.form-row.field-file_download') || document.querySelector('.field-file_download');

    function updateFieldVisibility() {
        const val = contentTypeSelect.value;

        // Reset display
        if (rowHtml) rowHtml.style.display = 'none';
        if (rowPdf) rowPdf.style.display = 'none';
        if (rowExternal) rowExternal.style.display = 'none';
        if (rowInternal) rowInternal.style.display = 'none';
        if (rowDownload) rowDownload.style.display = 'none';

        if (val === 'html') {
            if (rowHtml) rowHtml.style.display = '';
        } else if (val === 'pdf') {
            if (rowPdf) rowPdf.style.display = '';
        } else if (val === 'external_link') {
            if (rowExternal) rowExternal.style.display = '';
        } else if (val === 'internal_link') {
            if (rowInternal) rowInternal.style.display = '';
        } else if (val === 'file_download') {
            if (rowDownload) rowDownload.style.display = '';
        } else if (val === 'dropdown_only') {
            // No content needed
        }
    }

    contentTypeSelect.addEventListener('change', updateFieldVisibility);
    updateFieldVisibility();
});

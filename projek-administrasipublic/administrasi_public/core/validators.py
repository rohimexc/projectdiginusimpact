import os
from django.core.exceptions import ValidationError
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_IMAGE_MIMES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.webm', '.ogg'}
ALLOWED_VIDEO_MIMES = {'video/mp4', 'video/webm', 'video/ogg'}
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_PDF_EXTENSIONS = {'.pdf'}
ALLOWED_PDF_MIMES = {'application/pdf'}
MAX_PDF_SIZE = 20 * 1024 * 1024  # 20 MB

ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'}
ALLOWED_DOCUMENT_MIMES = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/octet-stream',  # Sebagian browser mengirim octet-stream untuk .docx/.xlsx
}
MAX_DOCUMENT_SIZE = 25 * 1024 * 1024  # 25 MB


def _get_extension(file):
    return os.path.splitext(getattr(file, 'name', ''))[1].lower()


def _peek_header(file, length=32):
    pos = file.tell() if hasattr(file, 'tell') else 0
    file.seek(0)
    header = file.read(length)
    file.seek(pos)
    return header


def validate_image_file(file):
    """Validasi gambar (ekstensi, ukuran maks 10 MB, MIME type, dan verifikasi isi gambar asli)."""
    if not file:
        return
    ext = _get_extension(file)
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError('Format gambar tidak diizinkan! Hanya menerima JPG, JPEG, PNG, atau WEBP.')

    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError('Ukuran gambar terlalu besar! Maksimal 10 MB.')

    content_type = getattr(file, 'content_type', None)
    if content_type and content_type.lower() not in ALLOWED_IMAGE_MIMES:
        raise ValidationError('Tipe MIME file gambar tidak valid.')

    # Verifikasi isi file benar-benar gambar yang sah menggunakan Pillow
    try:
        pos = file.tell() if hasattr(file, 'tell') else 0
        file.seek(0)
        img = Image.open(file)
        img.verify()
        file.seek(pos)
    except Exception:
        raise ValidationError('Berkas gambar rusak atau bukan file gambar yang valid!')


def validate_video_file(file):
    """Validasi video (ekstensi MP4/WebM/Ogg, ukuran maksimal 100 MB, MIME & header signature)."""
    if not file:
        return
    ext = _get_extension(file)
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError('Format video tidak diizinkan! Hanya menerima MP4, WEBM, atau OGG.')

    if file.size > MAX_VIDEO_SIZE:
        raise ValidationError('Ukuran video terlalu besar! Maksimal 100 MB.')

    content_type = getattr(file, 'content_type', None)
    if content_type and content_type.lower() not in ALLOWED_VIDEO_MIMES:
        raise ValidationError('Tipe MIME file video tidak valid.')

    header = _peek_header(file, 16)
    if ext == '.mp4' and b'ftyp' not in header:
        raise ValidationError('Berkas tidak valid sebagai video MP4!')
    if ext == '.webm' and not header.startswith(b'\x1a\x45\xdf\xa3'):
        raise ValidationError('Berkas tidak valid sebagai video WebM!')
    if ext == '.ogg' and not header.startswith(b'OggS'):
        raise ValidationError('Berkas tidak valid sebagai video Ogg!')


def validate_pdf_file(file):
    """Validasi khusus file PDF (ekstensi, ukuran maks 20 MB, header %PDF-)."""
    if not file:
        return
    ext = _get_extension(file)
    if ext not in ALLOWED_PDF_EXTENSIONS:
        raise ValidationError('Format file tidak diizinkan! Hanya menerima dokumen PDF (.pdf).')

    if file.size > MAX_PDF_SIZE:
        raise ValidationError('Ukuran file PDF terlalu besar! Maksimal 20 MB.')

    content_type = getattr(file, 'content_type', None)
    if content_type and content_type.lower() not in ALLOWED_PDF_MIMES:
        raise ValidationError('Tipe MIME file PDF tidak valid.')

    header = _peek_header(file, 8)
    if not header.startswith(b'%PDF-'):
        raise ValidationError('Isi berkas bukan file PDF yang valid!')


def validate_document_file(file):
    """Validasi dokumen akademik (PDF, Word, Excel, PowerPoint, maks 25 MB)."""
    if not file:
        return
    ext = _get_extension(file)
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(
            'Format dokumen tidak diizinkan! Hanya menerima PDF, DOC, DOCX, XLS, XLSX, PPT, atau PPTX.'
        )

    if file.size > MAX_DOCUMENT_SIZE:
        raise ValidationError('Ukuran dokumen terlalu besar! Maksimal 25 MB.')

    content_type = getattr(file, 'content_type', None)
    if content_type and content_type.lower() not in ALLOWED_DOCUMENT_MIMES:
        raise ValidationError('Tipe MIME dokumen tidak valid.')

    header = _peek_header(file, 16)
    lower_header = header.lower()
    if any(sig in lower_header for sig in (b'<?php', b'<script', b'<html', b'mz\x90', b'#!')):
        raise ValidationError('Berkas ditolak demi keamanan sistem!')

    if ext == '.pdf' and not header.startswith(b'%PDF-'):
        raise ValidationError('Isi berkas bukan file PDF yang valid!')
    if ext in {'.docx', '.xlsx', '.pptx'} and not header.startswith(b'PK'):
        raise ValidationError('Isi berkas Office OpenXML (.docx/.xlsx/.pptx) tidak valid!')
    if ext in {'.doc', '.xls', '.ppt'} and not header.startswith(b'\xd0\xcf\x11\xe0'):
        raise ValidationError('Isi berkas Office (.doc/.xls/.ppt) tidak valid!')


# =========================================================================
# VALIDATOR SITE SETTINGS (FAVICON & LOGO WEBSITE)
# =========================================================================
ALLOWED_FAVICON_EXTENSIONS = {'.png', '.ico', '.svg', '.jpg', '.jpeg', '.webp'}
MAX_FAVICON_SIZE = 500 * 1024  # 500 KB

ALLOWED_LOGO_EXTENSIONS = {'.png', '.webp', '.svg', '.jpg', '.jpeg'}
MAX_LOGO_SIZE = 2 * 1024 * 1024  # 2 MB


def validate_favicon_file(file):
    """Validasi favicon website (ekstensi .png, .ico, .svg, .jpg, .webp, maks 500 KB)."""
    if not file:
        return
    ext = _get_extension(file)
    if ext not in ALLOWED_FAVICON_EXTENSIONS:
        raise ValidationError('Format favicon tidak diizinkan! Rekomendasi: .png, .ico, atau .svg.')

    if file.size > MAX_FAVICON_SIZE:
        raise ValidationError('Ukuran favicon terlalu besar! Maksimal 500 KB agar website tetap cepat dimuat.')

    if ext in {'.png', '.jpg', '.jpeg', '.webp'}:
        try:
            pos = file.tell() if hasattr(file, 'tell') else 0
            file.seek(0)
            img = Image.open(file)
            img.verify()
            file.seek(pos)
        except Exception:
            raise ValidationError('Berkas favicon rusak atau bukan file gambar yang valid!')


def validate_site_logo_file(file):
    """Validasi logo header & footer website (ekstensi .png, .webp, .svg, .jpg, .jpeg, maks 2 MB)."""
    if not file:
        return
    ext = _get_extension(file)
    if ext not in ALLOWED_LOGO_EXTENSIONS:
        raise ValidationError('Format logo tidak diizinkan! Rekomendasi: .png, .webp, atau .svg (transparan).')

    if file.size > MAX_LOGO_SIZE:
        raise ValidationError('Ukuran file logo terlalu besar! Maksimal 2 MB.')

    if ext in {'.png', '.jpg', '.jpeg', '.webp'}:
        try:
            pos = file.tell() if hasattr(file, 'tell') else 0
            file.seek(0)
            img = Image.open(file)
            img.verify()
            file.seek(pos)
        except Exception:
            raise ValidationError('Berkas logo rusak atau bukan file gambar yang valid!')



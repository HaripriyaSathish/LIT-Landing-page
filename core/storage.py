"""
Image storage that uploads to Cloudinary using the credentials saved in
Admin → Site Settings. Until Cloudinary is configured there, files are kept
in the local MEDIA_ROOT so the admin keeps working.

Cloudinary files are stored by their full secure URL; local files by their
relative path.
"""
import re
from urllib.request import urlopen

import cloudinary
import cloudinary.uploader
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.deconstruct import deconstructible

CLOUDINARY_URL_RE = re.compile(r'/upload/(?:[^/]+/)*?v\d+/(?P<public_id>.+?)(?:\.[a-zA-Z0-9]+)?$')


def configure_cloudinary():
    """Configure the Cloudinary SDK from Site Settings. Returns True if enabled."""
    from core.models import SiteSettings

    site = SiteSettings.objects.filter(pk=1).first()
    if not site or not site.cloudinary_is_ready:
        return False
    cloudinary.config(
        cloud_name=site.cloudinary_cloud_name,
        api_key=site.cloudinary_api_key,
        api_secret=site.cloudinary_api_secret,
        secure=True,
    )
    return True


def is_remote(name):
    return bool(name) and name.startswith(('http://', 'https://'))


@deconstructible
class CloudinaryOrLocalStorage(Storage):
    def __init__(self, folder='lit'):
        self.folder = folder

    @property
    def local(self):
        return FileSystemStorage()

    def _save(self, name, content):
        if configure_cloudinary():
            content.seek(0)
            result = cloudinary.uploader.upload(
                content,
                folder=f'lit/{self.folder}',
                resource_type='image',
                use_filename=True,
                unique_filename=True,
            )
            return result['secure_url']
        return self.local._save(name, content)

    def _open(self, name, mode='rb'):
        if is_remote(name):
            with urlopen(name) as response:
                return ContentFile(response.read(), name=name.rsplit('/', 1)[-1])
        return self.local._open(name, mode)

    def delete(self, name):
        if not name:
            return
        if is_remote(name):
            match = CLOUDINARY_URL_RE.search(name)
            if match and configure_cloudinary():
                try:
                    cloudinary.uploader.destroy(match.group('public_id'))
                except Exception:
                    pass
            return
        self.local.delete(name)

    def exists(self, name):
        return False if is_remote(name) else self.local.exists(name)

    def url(self, name):
        if not is_remote(name):
            return self.local.url(name)
        # f_auto = WebP/AVIF when the browser supports it, q_auto = optimised quality
        if 'res.cloudinary.com' in name and '/upload/' in name and 'f_auto' not in name:
            return name.replace('/upload/', '/upload/f_auto,q_auto/', 1)
        return name

    def size(self, name):
        return 0 if is_remote(name) else self.local.size(name)

    def path(self, name):
        if is_remote(name):
            raise NotImplementedError('Cloudinary files have no local path.')
        return self.local.path(name)

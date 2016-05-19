import os

import furl

from mfr.core import utils
from mfr.core import extension

from mfr.extensions.latex import settings

class LatexRenderer(extension.BaseRenderer):
    def __init__(self, metadata, file_path, url, assets_url, export_url):
        super().__init__(metadata, file_path, url, assets_url, export_url)

        self.export_file_path = self.file_path + settings.RENDERER

        exported_url = furl.furl(export_url)
        exported_url.args['format'] = settings.FORMAT
        exported_metadata = self.metadata
        exported_metadata.download_url = exported_url.url

        self.renderer = utils.make_renderer(
            settings.RENDERER,
            exported_metadata,
            self.export_file_path,
            exported_url.url,
            assets_url,
            export_url
        )

    def render(self):
        if self.renderer.file_required:
            exporter = utils.make_exporter(
                self.metadata.ext,
                self.file_path,
                self.export_file_path,
                settings.FORMAT
            )
            exporter.export()

        rendition = self.renderer.render()

        if self.renderer.file_required:
            try:
                os.remove(self.export_file_path)
            except FileNotFoundError:
                pass

        return rendition

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

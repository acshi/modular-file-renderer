import subprocess
import os
import tempfile

from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.latex import settings


class LatexExporter(extension.BaseExporter):

    def export(self):
        dir_name = os.path.dirname(self.output_file_path)
        file_name = os.path.basename(self.output_file_path)
        job_name = os.path.splitext(file_name)[0]

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            # a single rerun is often necessary to get references correct
            run_times = 0
            rerun = True
            while rerun and run_times < settings.MAX_RUN_TIMES:
                run_times += 1
                result = subprocess.run([
                    settings.PDFLATEX_BIN,
                    '-interaction=nonstopmode',
                    '-output-directory=' + tmp_dir_name,
                    '-jobname=' + job_name,
                    self.source_file_path
                ], stdout = subprocess.PIPE)
                rerun = settings.RERUN_STRING in result.stdout

            # don't check return status as pdflatex almost always reports an error
            output_pdf_path = os.path.join(tmp_dir_name, file_name)
            if not os.path.exists(output_pdf_path):
                raise exceptions.ExporterError('Unable to export the file in the requested format, please try again later.', code=400)

            os.rename(output_pdf_path , self.output_file_path)

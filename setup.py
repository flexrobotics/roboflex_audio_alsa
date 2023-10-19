import sys
import os
import subprocess
import platform
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection & inclusion of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']

        self.build_temp = os.path.join(os.path.abspath(self.build_temp), 'build')
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

setup(
    name='roboflex.audio_alsa',
    version='0.1.0',
    description='Roboflex Audio input library using ALSA',
    author='Colin Prepscius',
    author_email='colinprepscius@gmail.com',
    url="https://github.com/flexrobotics/roboflex_audio_alsa",
    long_description="Roboflex Audio input library using ALSA",
    classifiers = [],
    keywords = [],
    license = "MIT",
    python_requires='>=3.6',
    install_requires=['numpy', 'roboflex'],
    ext_modules=[CMakeExtension('roboflex/audio_alsa/roboflex_audio_alsa_ext')],
    cmdclass=dict(build_ext=CMakeBuild),
    py_modules=['__init__'],
    packages=['roboflex.audio_alsa'],
    package_dir={'roboflex.audio_alsa': 'python'}
)

from setuptools import setup, find_packages
from setuptools.command.develop import develop
import pathlib
import os
from subprocess import check_call


def generate_proto_code():
    proto_interface_dir = "./src/interfaces"
    generated_src_dir = "./src/generated/"
    out_folder = "src"
    if not os.path.exists(generated_src_dir):
        os.mkdir(generated_src_dir)
    proto_it = pathlib.Path().glob(proto_interface_dir + "/**/*")
    proto_path = "generated=" + proto_interface_dir
    protos = [str(proto) for proto in proto_it if proto.is_file()]
    check_call(["protoc"] + protos + ["--python_out", out_folder, "--proto_path", proto_path])


class CustomDevelopCommand(develop):
    """Wrapper for custom commands to run before package installation."""
    uninstall = False

    def run(self):
        develop.run(self)

    def install_for_development(self):
        develop.install_for_development(self)
        generate_proto_code()


setup(
    name='python-protobuf',
    version='',
    package_dir={'': 'src'},
    cmdclass={
        'develop': CustomDevelopCommand, # used for pip install -e ./
    },
    packages=find_packages(where='src'),
    url='',
    license='',
    author='akshay.mathur',
    author_email='',
    description=''
)

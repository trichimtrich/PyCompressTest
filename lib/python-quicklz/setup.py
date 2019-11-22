from distutils.core import setup, Extension

setup(
    name = "python_quicklz",
    version = "1.5.0",
    description="QuickLZ Bindings for Python",
    author='Sergey Dryabzhinsky',
    author_email='sergey.dryabzhinsky@gmail.com',
    url='https://github.com/sergey-dryabzhinsky/python-quicklz',
    ext_modules = [
        Extension(
            "python_quicklz",
            ["quicklz.c", "quicklzpy.c"],
            extra_compile_args=[
               "-O2",
               "-std=c99",
               "-Wall",
               "-W",
               "-Wundef",
#           try fortification
#            "-DFORTIFY_SOURCE=2", "-fstack-protector",
#           try hard CPU optimization
#            "-march=native",
#           try Graphite
#            "-floop-interchange", "-floop-block", "-floop-strip-mine", "-ftree-loop-distribution",
            ]
        )
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)

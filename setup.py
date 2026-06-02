from setuptools import setup, find_packages

setup(
        name='OpenChemIE',
        version='0.1.0',
        author='Alex Wang',
        author_email='wang7776@mit.edu',
        url='https://github.com/CrystalEye42/OpenChemIE',
        packages=find_packages(),
        package_dir={'openchemie': 'openchemie'},
        python_requires='>=3.9',
        install_requires=[
            "numpy",
            "torch>=2.0",
            "transformers>=4.6.0",
            "layoutparser[effdet]",
            "pdf2image",
            "pypdf",
            "pdftotext",
            "pdfminer.six",
            "pandas",
            "matplotlib",
            "rdkit",
            "opencv-python",
            "Pillow",
            "ipython",
            "RxnScribe @ git+https://github.com/Ozymandias314/MolDetect.git",
            "MolScribe @ git+https://github.com/CrystalEye42/MolScribe.git@250f683",
            "ChemIENER @ git+https://github.com/Ozymandias314/ChemIENER.git",
            "chemrxnextractor @ git+https://github.com/CrystalEye42/ChemRxnExtractor.git@0f9529d",
            ],
        dependency_links=[
            "git+https://github.com/Ozymandias314/MolDetect.git",
            "git+https://github.com/CrystalEye42/MolScribe.git@250f683",
            "git+https://github.com/jiangfeng1124/ChemRxnExtractor.git",
        ])


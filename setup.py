from setuptools import setup, find_packages

setup(
    name="cxai",
    version="1.0.0",
    description="C-XAI: Clinical Explainable AI Quantitative Evaluation Benchmark",
    author="Sheela Akshar Sakhi, Dr. G. R. Ramya",
    author_email="cb.sc.u4cse23547@cb.students.amrita.edu",
    url="https://github.com/aksharsakhi/c-xai-healthcare-predictions",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.4.0",
        "scipy>=1.11.0",
        "shap>=0.44.0",
        "lime>=0.2.0.1",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps."
    ],
)

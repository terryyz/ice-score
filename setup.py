from setuptools import setup, find_packages

setup(
    name="llm_code_eval",
    version="0.1.0",
    author="Terry Yue Zhuo",
    author_email="terry.zhuo@monash.edu",
    description="MVP implementation of large-language-model-based code evaluation.",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    keywords='LLM, code generation, code evaluation, code quality',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "evaluate = llm_code_eval.evaluator:evaluate",
        ],
    },
)

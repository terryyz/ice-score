# Large Language Models Are State-of-the-art Evaluators Of Code Generation


## News


- 28/04/2023. Preprint is online.
- 24/04/2023. Drafting the preprint.
- 22/04/2023. Experiments starts.


## Paper
[Original Version](assets/paper.pdf)


## Abstract


Recent advancements in the field of natural language generation have facilitated the use of large language models to assess the quality of generated text. Although these models have shown promising results in tasks such as machine translation and summarization, their applicability in code generation tasks remains limited without human involvement. The complexity of programming concepts required for such tasks makes it difficult to develop evaluation metrics that align with human judgment. Token-matching-based metrics, such as BLEU, have demonstrated weak correlations with human practitioners in code generation tasks. Moreover, the utilization of human-written test suites to evaluate functional correctness can be challenging in domains with low resources. To overcome these obstacles, we propose a new evaluation framework based on the GPT-3.5 (`GPT-3.5-turbo`), for code generation assessments. Our framework addresses the limitations of existing approaches by achieving superior correlations with functional correctness and human preferences, without the need for test oracles or references. We evaluate the efficacy of our framework on two different tasks and four programming languages, comparing its performance with the state-of-the-art CodeBERTScore metric, which relies on a pre-trained model. Our results demonstrate that our framework surpasses CodeBERTScore, delivering high levels of accuracy and consistency across various programming languages and tasks. We encourage further research in the evaluation of code generation.


## Overview


![framework](assets/framework.png)
Our framework assesses code generation from two aspects:
- **Human-based Usefulness**: Usefulness of the code snippet based on the problem description.
- **Execution-based Functional Correctness**: Execution-based quality of the code snippet combined with the problem.


## Environment Setup
Our experiment is mainly built on the [codegen-metrics](https://github.com/JetBrains-Research/codegen-metrics) and [code-bert-score](https://github.com/neulab/code-bert-score) repositories. To replicate all experiments, please follow their instructions to set up the environment.


To run `compute_results.ipynb` and modules in `llm-code-eval` folder, use the following command to install all dependencies:
```bash
pip install -r requirements.txt
```


## Folder Description
- `data/` contains all processed data used in the paper.
    - `data/conala/` contains the CoNaLa dataset with all automatic evaluation results.
    - `data/humaneval/` contains the HumanEval dataset with all automatic evaluation results.
      - `data/humaneval/humaneval_java_grade.json`: Java split
      - `data/humaneval/humaneval_cpp_grade.json`: C++ split
      - `data/humaneval/humaneval_python_grade.json`: Python split
      - `data/humaneval/humaneval_js_grade.json`: JavaScript split
 
- `experiment_source/` contains the scripts to collect all automatic evaluation results. They require specific modifications to run on your machine. Note that for any of these scripts using `metrics_evaluation.metrics`, you need to use the implementations in `metrics_evaluation` folder from [codegen-metrics](https://github.com/JetBrains-Research/codegen-metrics).


- `llm_code_eval` contains the implementation of a minimum viable product (MVP) of this project. You are able to use it to evaluation any generated code snippet. Please refer to the `Use Large Language Models To Downstream Tasks Of Source Code` or more details.


## Use Large Language Models To Evaluate Downstream Tasks Of Source Code
We implement a minimum viable product (MVP) of this project. To install the project, please use the following command:
```bash
pip install -e .
```
You can use it to evaluate any generated code snippet, with the inputs of `problem`, `output`, `task`, `aspect` and `model`, like the following example:
```python
from llm_code_eval import evaluate

score = evaluate(problem="Given a list of integers, return the sum of all the integers.", output="sum = 0\nfor i in range(len(list)):\n\tsum += list[i]\nreturn sum", task="code-gen", aspect="usefulness", model="gpt-3.5-turbo")

print(score)
```

If you want to evaluate with reference code, you can use the option of `reference` in the following example:
```python
from llm_code_eval import evaluate

score = evaluate(problem="Given a list of integers, return the sum of all the integers.", output="sum = 0\nfor i in range(len(list)):\n\tsum += list[i]\nreturn sum", reference="sum = 0\nfor i in range(len(list)):\n\tsum += list[i]\nreturn sum", task="code-gen", aspect="usefulness", model="gpt-3.5-turbo")

print(score)
```


You can also use the option of `cot=True` to enable the zero-shot chain-of-thought evaluation in the following example:
```python
from llm_code_eval import evaluate

score, eval_step = evaluate(problem="Given a list of integers, return the sum of all the integers.", output="sum = 0\nfor i in range(len(list)):\n\tsum += list[i]\nreturn sum", task="code-gen", aspect="usefulness", model="gpt-3.5-turbo", cot=True)

print(score)
print(eval_step)
```
## Call For Contributions
The MVP requires a lot of improvements in terms of the design, and the diversity of the evaluation tasks (with the proper prompts).


We welcome any contributions to this project. Please feel free to open an issue or submit a pull request.


## Acknowledgement
We thank [JetBrains Research](https://research.jetbrains.org/) and [NeuLab](http://www.cs.cmu.edu/~neulab/) for their open-source code and data.


## Citation
```
@article{zhuo2023large,
  title={Large Language Models Are State-of-the-art Evaluators Of Code Generation},
  author={Zhuo, Terry Yue},
  journal={arXiv preprint arXiv:2302},
  year={2023}
}
```
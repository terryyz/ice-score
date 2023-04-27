import json
from glob import glob
from tqdm import tqdm
import random
from metrics_evaluation.metrics import (
    codebleu,
)


if __name__ == "__main__":
    for file in glob("data/*cpp*-0.8-keep")[:]:
        language = file.replace("data/","").split("_")[1]
        
        with open(file+"/human_grade.json") as f:
            data=json.load(f)
        try:
            with open(f"{language}_humaneval_codebleu.json") as f:
                orginal_results = json.load(f)
                length=len(orginal_results)
        except:
            orginal_results=[]
            length=0
        print(language,length)
        for _,d in enumerate(tqdm(data[length:])):
            tmp_results=[]
            intent=d['intent']
            snippet=d['snippet'][0]
            inputs = []
            ks = []
            for k in list(d.keys()):
                if k.isnumeric():
                    ks.append(k)
                    inputs.append(d[k])
            try:
                random.seed(42)
                idx = random.sample(range(len(inputs)), 20)
                inputs = [inputs[i] for i in idx]
                ks = [ks[i] for i in idx]
            except:
                pass
            results = dict()
            outs = [codebleu(snippet.strip(),inp.strip()) for inp in inputs]
            [results.update({f"grade-{k}": d[f"grade-{k}"],
                        f"codebleu-{k}": outs[i]})
                            for i,k in enumerate(ks)]
            orginal_results.append(results) 
            with open(f"{language}_humaneval_codebleu.json", "w") as f:
                json.dump(orginal_results, f, indent=4)

import json
from glob import glob
from tqdm import tqdm
import random
from metrics_evaluation.metrics import (
    sentence_chrf,
)


if __name__ == "__main__":
    for file in glob("data/*-0.8-keep")[:]:
        language = file.replace("data/","").split("_")[1]
        
        with open(file+"/human_grade.json") as f:
            data=json.load(f)

        orginal_results=[]
        length=0
        print(language,length)
        for _,d in enumerate(tqdm(data)):
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
            outs = [sentence_chrf(inp,[snippet]).score / 100 for inp in inputs]
            [results.update({f"grade-{k}": d[f"grade-{k}"],
                        f"chrf-{k}": outs[i]})
                            for i,k in enumerate(ks)]
            orginal_results.append(results) 
            with open(f"{language}_humaneval_chrf.json", "w") as f:
                json.dump(orginal_results, f, indent=4)

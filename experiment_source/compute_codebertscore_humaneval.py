import json
from glob import glob
from tqdm import tqdm
import random
import code_bert_score as cbs

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
            try:
                # P, R, F1, F3 = cbs.score(cands=inputs, refs=[snippet]*len(inputs), lang=language)
                P, R, F1, F3 = cbs.score(cands=inputs, refs=[snippet]*len(inputs), sources=[intent]*len(inputs), lang=language)
                results = dict()
                [results.update({f"grade-{k}": d[f"grade-{k}"],
                            f"codebertscore-{k}": {"P": P.tolist()[i], 
                                                        "R": R.tolist()[i], 
                                                        "F1": F1.tolist()[i], 
                                                        "F3": F3.tolist()[i]
                                                        }})
                                for i,k in enumerate(ks)]
            except:
                P, R, F1, F3=[],[],[],[]
                for i in range(len(ks)):
                    try:
                        # p, r, f1, f3 = cbs.score(cands=[inputs[i]], refs=[snippet], lang=language)
                        p, r, f1, f3 = cbs.score(cands=[inputs[i]], refs=[snippet], sources=[intent], lang=language)
                        P.append(p.tolist()[0])
                        R.append(r.tolist()[0])
                        F1.append(f1.tolist()[0])
                        F3.append(f3.tolist()[0])
                    except:
                        P.append(0)
                        R.append(0)
                        F1.append(0)
                        F3.append(0)
                results = dict()
                [results.update({f"grade-{k}": d[f"grade-{k}"],
                            f"codebertscore-{k}": {"P": P[i], 
                                                        "R": R[i], 
                                                        "F1": F1[i], 
                                                        "F3": F3[i]
                                                        }})
                                for i,k in enumerate(ks)]
            orginal_results.append(results) 
            with open(f"{language}_humaneval_codebertscore_intent.json", "w") as f:
                json.dump(orginal_results, f, indent=4)

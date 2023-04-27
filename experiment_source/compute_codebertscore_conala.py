import json
from glob import glob
from tqdm import tqdm
import random
import code_bert_score as cbs

if __name__ == "__main__":
    conala_models_list = ['baseline', 'tranx-annot', 'best-tranx', 'best-tranx-rerank', 'codex']
    with open('data/to-grade/conala/conala-human-grades.json') as f:
        data = json.load(f)
    try:
        with open("conala_codebertscore.json") as f:
            orginal_results=json.load(f)
        length=len(orginal_results)
    except:
        orginal_results=[]
        length=0
    results=[]
    for d in tqdm(data[length:]):
        intent=d['intent']
        snippet=d['snippet'][0]
        inputs = []
        for k in conala_models_list:
            inputs.append(d[k])
        try:
            P, R, F1, F3 = cbs.score(cands=inputs, refs=[snippet]*len(conala_models_list), lang="python")
            results = dict()
            [results.update({f"grade-{k}": d[f"grade-{k}"],
                        f"codebertscore-grade-{k}": {"P": P.tolist()[i], 
                                                    "R": R.tolist()[i], 
                                                    "F1": F1.tolist()[i], 
                                                    "F3": F3.tolist()[i]
                                                    }})
                            for i,k in enumerate(conala_models_list)]
        except:
            P, R, F1, F3=[],[],[],[]
            for i in range(len(conala_models_list)):
                try:
                    p, r, f1, f3 = cbs.score(cands=[inputs[i]], refs=[snippet], lang="python")
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
                        f"codebertscore-grade-{k}": {"P": P[i], 
                                                    "R": R[i], 
                                                    "F1": F1[i], 
                                                    "F3": F3[i]
                                                    }})
                            for i,k in enumerate(conala_models_list)]
        
        orginal_results.append(results) 
        with open("conala_codebertscore.json", "w") as f:
            json.dump(orginal_results, f, indent=4)
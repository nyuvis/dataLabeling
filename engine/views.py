from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
import json
import numpy as np
import gensim
import csv
import smart_open
import re
import random
import os

from django.urls import reverse
from sklearn.manifold import TSNE
from sklearn import svm
from scipy.stats import entropy
import joblib

#render Page
def index(request):
    next_instance_id = list(unlabeledSet.keys())[0]
    context = {'data_dict': data_dict[next_instance_id], 'next_instance_id': json.dumps(next_instance_id)}
    return render(request, 'engine/index.html', context)

def visSel(request):
    context = {'data_dict': dict_slice(data_dict,2000,5000)}
    return render(request, 'engine/visSel.html', context)

def updateClassifier():
    trainingSet_label = []
    training_vector_list = []
    global unlabeledSet
    global ranked_unlabledSet_id
    global svmClassifier

    for key in list(labeledSet.keys()):
        trainingSet_label.append(labeledSet[key])
        training_vector_list.append(data_dict[key]['docVec'])

    if training_vector_list and trainingSet_label:
        svmClassifier.fit(training_vector_list, trainingSet_label)
    else:
        print('TrainingSet Invalid')
    
    updateClassifier_auxliary()
    # return JsonResponse({'unlabeledSet': unlabeledSet, 'rankedUnlabeled_id':ranked_unlabledSet_id})
    return

def updateClassifier_auxliary():
    global unlabeledSet
    global ranked_unlabledSet_id
    global svmClassifier
    unlabeledSet_entropy_temp = []
    unlabeledSet_keys_list = list(unlabeledSet.keys())
    for key in unlabeledSet_keys_list:
        prob = svmClassifier.predict_proba([data_dict[key]['docVec']])[0]
        entropy_v = entropy(prob)
        predicted_cat = svmClassifier.predict([data_dict[key]['docVec']])[0]
        unlabeledSet[key] = {'index':key, 'prob': list(prob), 'entropy': entropy_v, 'predicted_cat':predicted_cat}
        data_dict[key]['prob'] = list(prob)
        data_dict[key]['entropy'] = entropy_v
        unlabeledSet_entropy_temp.append(entropy_v)
    # sorted(unlabeledSet.items(), key = lambda item: item[1]['entropy'], reverse=True)
    for key in labeledSet:
        prob = svmClassifier.predict_proba([data_dict[key]['docVec']])[0]
        entropy_v = entropy(prob)
        predicted_cat = svmClassifier.predict([data_dict[key]['docVec']])[0]
        data_dict[key]['prob'] = list(prob)
        data_dict[key]['entropy'] = entropy_v
        data_dict[key]['predicted_cat'] = predicted_cat
    
    unlabeledSet_entropy_temp  = np.array(unlabeledSet_entropy_temp)
    unlabeledSet_rank = np.argsort(-unlabeledSet_entropy_temp)
    ranked_unlabledSet_id = []
    for i in range(0, len(unlabeledSet_rank)):
        ranked_unlabledSet_id.append(unlabeledSet_keys_list[unlabeledSet_rank[i]])
    return

def classifierVis(request):
    global unlabeledSet
    global ranked_unlabledSet_id
    
    context = {'data_dict': dict_slice(data_dict,2000,5000), 'unlabeledSet': dict_slice(unlabeledSet,2000,5000), 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    # context = {'data_dict': data_dict, 'unlabeledSet': unlabeledSet, 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    return render(request, 'engine/classifierVis.html', context)

def radarVis(request):
    global unlabeledSet
    global ranked_unlabledSet_id
    
    context = {'data_dict': dict_slice(data_dict,2000,5000), 'unlabeledSet': dict_slice(unlabeledSet,2000,5000), 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    # context = {'data_dict': data_dict, 'unlabeledSet': unlabeledSet, 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    return render(request, 'engine/radarVis.html', context)

def parallelVis(request):
    global unlabeledSet
    global ranked_unlabledSet_id
    
    context = {'data_dict': dict_slice(data_dict,2000,5000), 'unlabeledSet': dict_slice(unlabeledSet,2000,5000), 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    # context = {'data_dict': data_dict, 'unlabeledSet': unlabeledSet, 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    return render(request, 'engine/parallelVis.html', context)

def dotVis(request):
    global unlabeledSet
    global ranked_unlabledSet_id
    
    context = {'data_dict': dict_slice(data_dict,2000,5000), 'unlabeledSet': unlabeledSet, 'labeledSet': labeledSet,'ranked_unlabledSet_id':ranked_unlabledSet_id, 'prob_Class':json.dumps(list(svmClassifier.classes_))}
    # context = {'data_dict': data_dict, 'unlabeledSet': unlabeledSet, 'labeledSet': labeledSet,'ranked_unlabledSet_id':ranked_unlabledSet_id, 'prob_Class':json.dumps(list(svmClassifier.classes_))}
    # context = {'data_dict': data_dict, 'unlabeledSet': unlabeledSet, 'ranked_unlabledSet_id':ranked_unlabledSet_id}
    return render(request, 'engine/dotVis.html', context)

def outputSometing(request):
    print(unlabeledSet[19234])
    print()
    return

def datasetOverview(request):
    context = {'data_dict': data_dict}
    return render(request, 'engine/datasetOverview.html', context)

def randomSampling(request):
    labeled_instance_id = int(request.GET.get('query_instance_id'))
    labeled_instance_label = request.GET.get('label_input')
    # print(request.GET.get('query_instance_id'))
    if unlabeledSet.__contains__(labeled_instance_id):
        pop_v = unlabeledSet.pop(labeled_instance_id)
        labeledSet[labeled_instance_id] = labeled_instance_label
        data_dict[labeled_instance_id]['isLabeled'] = 1
    else:
        labeledSet[labeled_instance_id] = labeled_instance_label

    next_instance_id = list(unlabeledSet.keys())[0]
    next_instance = data_dict[next_instance_id]
    context = {'next_instance': json.dumps(next_instance), 'next_instance_id': json.dumps(next_instance_id)}

    return JsonResponse(context)

def labelSingleDoc(request):
    labeled_instance_id = int(request.GET.get('query_instance_id'))
    labeled_instance_label = request.GET.get('label_input')
    # print(request.GET.get('query_instance_id'))
    if unlabeledSet.__contains__(labeled_instance_id):
        pop_v = unlabeledSet.pop(labeled_instance_id)
        labeledSet[labeled_instance_id] = labeled_instance_label
        data_dict[labeled_instance_id]['isLabeled'] = 1
    else:
        labeledSet[labeled_instance_id] = labeled_instance_label

    context = {}

    return JsonResponse(context)

def saveLabledDataToFile(request):
    global labeledSet
    global svmClassifier
    for key in list(labeledSet.keys()):
        np.append(idAndLabel_np,[key,labeledSet[key]])
    with open(labelRecord_path, 'wb') as f:
        np.save(f, np.array(idAndLabel_np))

    updateClassifier()
    joblib.dump(svmClassifier, svm_path)
    context = {}
    return JsonResponse(context)

def dict_slice(adict, start, end):
    keys = list(adict.keys())
    # print(keys)
    dict_slice = {}
    for k in keys[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice

dataset_name = 'yelp'
projectRoot_path = os.path.abspath('.')

# if dataset_name == 'yelp':
#     model_path = '/Users/hiphone/Documents/Code/datalabeling/suppport-file/model/yelp_90k_d100_e10.d2v'
#     doc_path = '/Users/hiphone/Documents/Code/datalabeling/suppport-file/text/Yelp-Ela/data_training.json'
#     coords_path = '/Users/hiphone/Documents/Code/datalabeling/suppport-file/coords/coords_tsne_2W.npy'
#     labelRecord_path = '/Users/hiphone/Documents/Code/datalabeling/suppport-file/labeled/labeled_data.npy'
#     svm_path = '/Users/hiphone/Documents/Code/datalabeling/suppport-file/labeled/svmFile.m'
#     graph_matrix_path = '/Users/hiphone/Documents/Code/datalabeling/suppport-file/labeled/graphMatrix.npy'
print(projectRoot_path)
if dataset_name == 'yelp':
    model_path = os.path.join(projectRoot_path,"suppport-file/model/yelp_90k_d100_e10.d2v")
    doc_path = os.path.join(projectRoot_path,'suppport-file/text/Yelp-Ela/data_training.json')
    coords_path = os.path.join(projectRoot_path,'suppport-file/coords/coords_tsne_2W.npy')
    labelRecord_path = os.path.join(projectRoot_path,'suppport-file/labeled/labeled_data.npy')
    svm_path = os.path.join(projectRoot_path,'suppport-file/labeled/svmFile.m')
    graph_matrix_path = os.path.join(projectRoot_path,'suppport-file/labeled/graphMatrix.npy')

#data init
data_dict = {}
unlabeledSet = {}
labeledSet = {}
ranked_unlabledSet_id = []
svmClassifier = svm.SVC(decision_function_shape='ovo', probability=True)

#Load Labeled Record
with open(labelRecord_path, 'rb') as f:
    idAndLabel_np = np.load(f)
    for item in idAndLabel_np:
        labeledSet[int(item[0])] = item[1]

#Load fundmental files
model = gensim.models.doc2vec.Doc2Vec.load(model_path)
coords = np.load(coords_path)

with open(doc_path, 'r') as f_train:
    #save data as dictionary
    t_dict = {}
    for index_data, line in enumerate(f_train.readlines()):
        if labeledSet.__contains__(index_data):
            isLabeled = 1
        else:
            isLabeled = 0
            unlabeledSet[index_data] = {'status':'toBeLabeled'}
        t_dict = {'index': index_data,'doc':json.loads(line)['text'], 'ori_cat':json.loads(line)['categories2'][0], 'docVec':model.docvecs[index_data].tolist(), 'coord': coords[index_data].tolist(), 'isLabeled':isLabeled}
        data_dict[index_data] = t_dict

svmClassifier = joblib.load(svm_path)
updateClassifier_auxliary()
#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import codecs
import docx
import spacy
from collections import Counter
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib


# In[65]:


class PACount:
    def __init__(self,path):
        self.path = path
        self.types = ["[ac]","[bc]","[ae]","[be]","[ag]","[bg]","[ai]","[bi]","[ak]","[bk]"]
        self.get_count()
        self._get_group_count()
        self.get_group_similarity()
        self._get_group_ab_count()
        self._get_group_nab_count_list()
        self.get_group_ab_similarity()
        self._get_group_ab_count_list()
    def get_group_name(self):
        return self.count_dict.keys()
    
    def get_group_nab_count(self):
        return self.no_ab_count
#     for i in group_name:
#     if i not in group_count:
#         group_count[i] = {}
#     for j in a.count_dict[i]:
#         for k in a.count_dict[i][j]:
#             if k not in group_count[i]:
#                 group_count[i][k] = 0
#             group_count[i][k] += a.count_dict[i][j][k]
            
            
    def _get_group_count(self):
        self.group_count = {}
        self.group_name = list(self.get_group_name())
        for i in self.group_name:
            if i not in self.group_count:
                self.group_count[i] = {}
                
            for j in self.count_dict[i]:
                for k in self.count_dict[i][j]:
                    if k not in self.group_count[i]:
                        self.group_count[i][k] = 0
                    self.group_count[i][k] += self.count_dict[i][j][k]
        self._get_group_count_list()
        
    def print_nab_group_plot(self):
        
        types = []
        for i in self.types:
            if i[2] not in types:
                types.append(i[2])
        for idx,i in enumerate(self.no_ab_count):
            print(i)
#             x = self.group_count_list[idx]
            x = []
            for j in self.no_ab_count[i]:
                x.append(self.no_ab_count[i][j])
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.bar(types,x)
            plt.savefig("noab_" + i +".pdf",dpi='figure',aspect='auto', bbox_inches = 'tight')
            plt.show()
            
            
    def print_ab_group_plot(self):
        
        types = []
        for i in self.types:
            if i[1] not in types:
                types.append(i[1])
        for idx,i in enumerate(self.ab_count):
            print(i)
#             x = self.group_count_list[idx]
            x = []
            for j in self.ab_count[i]:
                x.append(self.ab_count[i][j])
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.bar(types,x)
#             plt.legend()
            
            plt.savefig("ab_" + i +".pdf",dpi='figure',aspect='auto', bbox_inches = 'tight')
            plt.show()  
            
        
        
    def print_group_plot(self):

        for idx,i in enumerate(self.get_group_count()):
            print(i)
            x = self.group_count_list[idx]
        #     x = []
        #     for j in a.get_group_count()[i]:
        #         x.append(a.get_group_count()[i][j])
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.bar(self.types,x)
            plt.savefig("all_" + i +".pdf",dpi='figure',aspect='auto', bbox_inches = 'tight')
            plt.show()
            
            
#     def print_group_ab(self):
    def get_group_ab_count(self):
        return self.ab_count
    
    def _get_group_ab_count(self):
        self.no_ab_count = {}
        self.ab_count = {}
        for i in self.group_count:
            self.no_ab_count[i] = {}
            self.ab_count[i] = {}
            for j in self.group_count[i]:
                t = j[2]
                t1 = j[1]
                if t1 not in self.ab_count[i]:
                    self.ab_count[i][t1] = 0
                self.ab_count[i][t1] += self.group_count[i][j]
                if t not in self.no_ab_count[i]:
                    self.no_ab_count[i][t] = 0
                self.no_ab_count[i][t] += self.group_count[i][j]
                
    def cos_sim(self,a,b):
        return dot(a, b)/(norm(a)*norm(b))
    
    
    def print_cos_sim(self):
        for (i,j) in self.group_sim:
            print(i + " and " + j + " cosine similarity is :")
            print(self.group_sim[(i,j)])
            
    def print_nab_cos_sim(self):
        for (i,j) in self.group_no_ab_sim:
            print(i + " and " + j + " cosine similarity is :")
            print(self.group_no_ab_sim[(i,j)])
            
            
    def get_group_similarity(self):
        self.group_sim = {}
        for idx,i in enumerate(self.group_count):
            for jdx,j in enumerate(self.group_count):
                if i != j:
                    if (i,j) not in self.group_sim:
                        self.group_sim[(i,j)] = self.cos_sim(self.group_count_list[idx],self.group_count_list[jdx])
#                     print(i + " and " + j + " cosine similarity is :")
#                     print(self.cos_sim(self.group_count_list[idx],self.group_count_list[jdx]))


    def get_group_ab_similarity(self):
        self.group_no_ab_sim = {}
        for idx,i in enumerate(self.no_ab_count):
            for jdx,j in enumerate(self.no_ab_count):
                if i != j:
                    if (i,j) not in self.group_no_ab_sim:
                        self.group_no_ab_sim[(i,j)] = self.cos_sim(self.group_nab_count_list[idx],self.group_nab_count_list[jdx])        
        
    def get_group_count(self):
        return self.group_count
    
    def _get_group_nab_count_list(self):
        self.group_nab_count_list = []
        for i in self.no_ab_count:
            single = []
            for k in self.no_ab_count[i]:
                single.append(self.no_ab_count[i][k])
            self.group_nab_count_list.append(single)
            
            
    def _get_group_ab_count_list(self):
        self.group_ab_count_list = []
        for i in self.ab_count:
            single = []
            for k in self.ab_count[i]:
                single.append(self.ab_count[i][k])
            self.group_ab_count_list.append(single)
            
            
    def _get_group_count_list(self):
        self.group_count_list = []
        for i in self.group_count:
            single = []
            for k in self.group_count[i]:
                single.append(self.group_count[i][k])
            self.group_count_list.append(single)
            
    def get_group_count_list(self):
        return self.group_count_list
    
    def get_count(self):
#         path = "./final"
        # files_path = os.listdir("./data")
        # path = "./data/longterm"
        files_path = os.listdir(self.path)
        self.count_dict = {}
        self.times = {}
        self.w_count = {}
        self.token_num = {}
        for pa in files_path:
            if ".DS_Store" not in pa:
                folder_path = os.path.join(self.path,pa)
                self.count_dict[pa] = {}
                self.times[pa] = {}
                folders = os.listdir(folder_path)
                self.token_num[pa] = 0
                self.w_count[pa] = {}
                for t in self.types:
                    self.w_count[pa][t[1:3]] = Counter()
                for file in folders:
                    if file.endswith('docx'): 
                        self.count_dict[pa][file] = Counter()
                        file_path = os.path.join(folder_path,file)
                        doc = docx.Document(file_path)
                        sents = []
                        for i in doc.paragraphs:
                            sents.append(i.text)
                            if "TIMES:" in i.text:
                                line = i.text.replace("TIMES:","").strip().split(":")
        #                         times[pa][file] =i.text.replace("TIMES:","").strip()
        #                         line = times[i][j].split(":")
        #                         times[i][j] = (int(line[0]) + int(line[1])/60)
                                self.times[pa][file] = (int(line[0]) + int(line[1])/60)
                        for i in self.types:
                            self.count_dict[pa][file][i] = 0
                        for i in sents:
                            line = i.replace("\n","").split("**")
                            for idx,j in enumerate(line):
                                for t in self.types:
                                    if t in j:
                                        self.w_count[pa][t[1:3]][line[idx-1].replace("说话人","").replace("[bc]","").replace("[ac]","").lower().strip()] +=1
        #                 token_num[pa] = token(sents)
                        if "Chinese" in pa:
                            s = sents
                        for i in sents:
                            for j in self.types:
                                self.count_dict[pa][file][j] += i.count(j)
        


# In[66]:


path = "./final"


# In[67]:


# PACount(文件路径)
a = PACount(path)


# In[68]:


#输出group的similarity(重要
print("print group similarity")
a.print_cos_sim()
print("======================")
#输出group的similarity(不分ab的)
print("print similarity(no ab)")
a.print_nab_cos_sim()
print("======================")
print("print group count")
print(a.get_group_count())
print("======================")
print("print group count(no ab)")
print(a.no_ab_count)
print("======================")
# 输出group的数量(只分ab)
print("print group count(only ab)")
print(a.ab_count)
print("======================")
a.print_group_plot()
a.print_nab_group_plot()
a.print_ab_group_plot()


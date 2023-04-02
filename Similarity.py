#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity


# In[22]:


file = pd.read_excel(r"FinalData.xlsx")
df = file


# In[23]:


file.drop(columns='What is your name?', inplace=True)
file.drop(columns='What is your gender?', inplace=True)
file.drop(columns='What was your course in UG?', inplace=True)
file.drop(columns='What was the average CGPA or Percentage obtained in under graduation?', inplace=True)
#file.drop(columns='Have you done masters after undergraduation? If yes, mention your field of masters.(Eg, Masters in Mathematics)', inplace=True)


# In[24]:


file.rename(columns = {file.columns[0] :'UG_Course',
                       file.columns[1] :'Interest',
                       file.columns[2] :'Skills',
                       file.columns[3] :'Certification',
                       file.columns[4] :'Certificate_name',
                       file.columns[5] :'Working',
                       file.columns[6] :'JobTitle',
                       file.columns[7] :'Masters'
                      },inplace = True)


# In[25]:


file = file[file['Skills'].notna()]
file = file[file['Interest'].notna()]
file = file[file['Certificate_name'].notna()]
file["Skills"]=file["Skills"].astype(str)


# In[26]:


file.info()


# In[27]:


df = file


# In[28]:


df


# In[32]:


def recommend(d):
    global df
    
    d = pd.DataFrame([d])
    df = pd.concat([df, d], axis=0, ignore_index=True)
    
    df_last=df.iloc[[-1],]
    
    
    #df['Skills'] = df['Skills'].str.split(',')
    #df['Interest'] = df['Interest'].str.split(',')
    #df['Certificate_name'] = df['Certificate_name'].str.split(',')
    
    df['factors'] = df[['Interest','Skills']].apply("-".join, axis=1)
    
    i=0
    for i in range (len(df)):
        m_to_b = df.Certification[i]
        certi = df.Certificate_name[i]
        if m_to_b.startswith('Y') ==True:
            df.factors[i] = df.factors[i] + '-' + certi       
        i=i+1
        
    i=0
    for i in range (len(df)):
        m_to_b = df.Working[i]
        job = df.JobTitle[i]
        if m_to_b.startswith('Y') ==True:
            df.factors[i] = df.factors[i] + '-' + job      
        i=i+1 
    
    i=0
    for i in range (len(df)):
        m_to_b = df.Masters[i]
        if m_to_b.startswith('N') ==True:
            continue
        else:
            df.factors[i] = df.factors[i] + '-' + m_to_b     
        i=i+1
        
    df_f = df.factors
    df_f.replace("[^a-zA-Z]"," ",regex=True, inplace=True)
    df_f = df_f.to_frame()
    df_f.columns=['factors']
    
    df_f["factors"].isnull().sum() 
    tfidf = TfidfVectorizer(stop_words = "english")
    tfidf_matrix = tfidf.fit_transform(df_f["factors"])
    tfidf_matrix_df=pd.DataFrame.sparse.from_spmatrix(tfidf_matrix)
    df_final=tfidf_matrix_df
    
    y = df_final.iloc[:-2,:]
    
    sim_matrix=cosine_similarity(df_final.iloc[[-1],:],y)
    df_sim_matrix = pd.DataFrame(sim_matrix)
    sim_scores = list(enumerate(sim_matrix[0]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse = True)
    s_idx  =  [i[0] for i in sim_scores]
    s_scores =  [i[1] for i in sim_scores]
    sim_scores
    
    df_similar = pd.DataFrame(columns=["UG_Course", "Score"])
    df_similar["UG_Course"] = df.loc[s_idx, "UG_Course"]
    df_similar["Score"] = s_scores
    df_similar=df_similar.loc[(df_similar.UG_Course !='')]
    df_similar=df_similar.drop_duplicates(subset='UG_Course', keep="first")
    
    df_similar_N = df_similar.iloc[0:4+1,:]
    df_similar_N.reset_index(inplace = True)
    ca = df_similar_N['UG_Course'].values.tolist()
    
    return ca
    


# In[30]:


d={}
print("Enter your details:  \n")
nm = input("Enter your name:  ")
gen = input("Enter your gender:  ")
d['UG_Course']=''
d['Interest']=input("Enter the interests:  ")
d['Skills']=input("Enter the skills :  ")
d['Certification']=input("Did you do any certification courses additionally? :  ")
if (d['Certification']=='yes' or d['Certification']=='Yes'):
    d['Certificate_name']=input("If yes, please specify your certificate course title:  ")
d['Working']=input("Are you currently working or have you been emplyed before?e :  ")
if (d['Working']=='yes' or d['Working']=='Yes'):
    d['JobTitle']=input(" If yes, please enter Job Title :  ")
d['Masters']=input("Are you currently pursuing masters or have you persued higher education before :  ")


# In[33]:


a = recommend(d)
print(a)


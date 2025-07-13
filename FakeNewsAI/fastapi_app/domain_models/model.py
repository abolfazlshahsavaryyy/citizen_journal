from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.svm import LinearSVC
from fastapi_app.preprocessing.clean_data import clean_data
class News:
    def __init__(self,title,text):
        self.title=title
        self.text=text
    def predict_logistic_regression(self,model:LogisticRegression):
        news_list=[[self.title,self.text,"'subject","date",'label']]
        news_dataframe=pd.DataFrame(news_list,columns=['text','title','subject','date','label'])
        news_dataframe=clean_data(news_dataframe)
        
        logistic_label=model.predict(news_dataframe)
        return {
            "logistic regression label":int(logistic_label[0])
        }

    def predict_svc(self,model :LinearSVC):
        news_list=[[self.title,self.text,"'subject","date",'label']]
        news_dataframe=pd.DataFrame(news_list,columns=['text','title','subject','date','label'])
        news_dataframe=clean_data(news_dataframe)
        
        svc_label=model.predict(news_dataframe)
        label='False'
        if(svc_label[0]==0):
            label='False'
        else:
            label="True"
        return {
            "logistic regression label":int(svc_label[0]),
            "label":label
        }
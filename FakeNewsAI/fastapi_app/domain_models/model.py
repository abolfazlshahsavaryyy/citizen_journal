from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.svm import LinearSVC
from preprocessing.clean_data import clean_data

class News:
    def __init__(self,title,text):
        self.title=title
        self.text=text
    def predict_logistic_regression(self, model: LogisticRegression):
        news_list = [[self.title, self.text, "'subject", "date", 'label']]
        news_dataframe = pd.DataFrame(news_list, columns=['text', 'title', 'subject', 'date', 'label'])

        # Preprocess the data
        news_dataframe = clean_data(news_dataframe)

        # Get predicted probabilities
        probabilities = model.predict_proba(news_dataframe)  # shape: (n_samples, n_classes)
        predicted_class = model.predict(news_dataframe)[0]

        # Get the confidence of the predicted class
        confidence = probabilities[0][predicted_class]  # e.g., if class = 1, get proba for class 1

        return {
            "predicted_class": int(predicted_class),
            "confidence": round(float(confidence), 4),
            "message": f"The model is {round(confidence*100)}% confident that this news belongs to class {predicted_class}"
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
import os
from os.path import join
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from django.conf import settings


from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier


class ensemble:
    def __init__(self):
        #current_dir_path=os.path.dirname(os.path.realpath(__file__))
        #print("Current directory :: ",current_dir_path)
        #self.dataset_path = os.path.join(current_dir_path,"dataset.csv")
        #print("Current dataset path :: ",self.dataset_path)s
        self.dataset_path = join(settings.STATIC_ROOT,'dataset.csv')

    def runEAlgo(self, testData):
        self.dataset = pd.read_csv(self.dataset_path)
        training_features = ['Soil Type', 'Soil depth(cm)', 'ph', 'Bulk density Gm/cc', 'Ec (dsm-1)', 'Organic carbon (%)', 'Soil moisture retention  (%)', 'Available water capacity(m/m)', ' Infiltration rate cm/hr', ' Clay %']
        
        target=' Crops to be taken'
        #ENCODE STRING DATA INTO INTEGER
        soil_type=np.unique(self.dataset['Soil Type'])
        soil_type_mapping={label:idx for idx,label in enumerate(soil_type)}
        
        print(soil_type_mapping)
        self.dataset['Soil Type']=self.dataset['Soil Type'].map(soil_type_mapping)
        
        crops_to_be_taken = np.unique(self.dataset[' Crops to be taken'])
        #print(crops_to_be_taken)
        crops_to_be_taken_mapping={label:idx for idx,label in enumerate(crops_to_be_taken)}
        #print(crops_to_be_taken_mapping)
        self.dataset[' Crops to be taken']=self.dataset[' Crops to be taken'].map(crops_to_be_taken_mapping)
        X=self.dataset[training_features]

        XX = np.array(X)
        
        y=self.dataset[target]
        Y=np.array(y)

        
        estimators = []
        model1 = SVC()
        estimators.append( ("svm", model1) )

        model2 = MLPClassifier(solver='adam', alpha=1e-5,
                                    hidden_layer_sizes=(5, 2), max_iter=2000,random_state=1)

        estimators.append( ("mlp", model2))

       

        

        ensemble = VotingClassifier(estimators)
        ensemble.fit(XX,Y)

        reTest = ""
        for soil_t,soil_type_index_value in soil_type_mapping.items():
            if soil_t == testData.split(",")[0]:
                reTest=soil_type_index_value

        change_str = testData.split(",")[0]
# =============================================================================

        tData = testData.replace(change_str,str(reTest))
        tArray =[float(d) for d in tData.split(",")]
 

        output = ensemble.predict([tArray])
        
        print (output)

        class_label_name=""
        for crop_name,crop_name_index_value in crops_to_be_taken_mapping.items():
            if crop_name_index_value == output:
                class_label_name=crop_name
        
        print(class_label_name)
        return class_label_name
    

if __name__ == "__main__":
        testData = ['Deep black soil',100,7.7,1.5,1.9,0.3,35,0.26,1.3,44]
        ensbl = ensemble()
        ensbl.runEAlgo(testData)





        

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.utils import timezone
from django.http import JsonResponse
import json
from crop_name_recommendation.SVM import SVM
from crop_name_recommendation.neural_network import NeuralNetwork
from crop_name_recommendation.ensemble import ensemble

from collections import Counter

def index(request):
   return render(request, 'crop_name_recommendation/index.html')

def home(request):
   return render(request, 'crop_name_recommendation/home.html')

def svm(request):
   return render(request, 'crop_name_recommendation/svm.html')


def neuralnetwork(request):
   return render(request, 'crop_name_recommendation/neuralnetwork.html')


def ensembleTech(request):
   return render(request, 'crop_name_recommendation/ensemble.html')

def aboutus(request):
   return render(request, 'crop_name_recommendation/aboutus.html')

def contactus(request):
   return render(request, 'crop_name_recommendation/contactus.html')

def signup(request):
       if(request.method == 'GET'):
           return render(request, 'crop_name_recommendation/signup.html')
       else:
          if(request.method == 'POST'):
             user_first_name = request.POST.get('firstname')
             user_last_name = request.POST.get('lastname')
             gender = request.POST.get('Gender')
             userEmail = request.POST.get("email")
             userPassword = request.POST.get("password")
             users = User.objects.filter(user_email = userEmail)
             
             print(" User password :: ",userPassword," User email :: ",userEmail )
             message = "not mentioned"
             url_path = "library_management/login.html"
             if users.count() > 0 :
                for  user in users:   
                   if user.first_name != user_first_name and user.user_email != userEmail:
                      userDetail = User(first_name=user_first_name,last_name=user_last_name,gender=gender,user_email=userEmail,user_password=userPassword)
                      userDetail.save()
                      print("Not find user name :: ")
                      message = 'Registration successfully...'
                      url_path = 'crop_name_recommendation/login.html'
                      break
                   else:
                      url_path = 'crop_name_recommendation/signup.html'
                      message = 'This user name already use. Please try another user name!!..',
             else:
                   userDetail = User(first_name=user_first_name,last_name=user_last_name,gender=gender,user_email=userEmail,user_password=userPassword)
                   userDetail.save()
                   message = 'Registration successfully...'
                   url_path = 'crop_name_recommendation/login.html'
                  
                  
             template = loader.get_template(url_path)
             context = {
                   'message':message,
                   }
             return HttpResponse(template.render(context,request)) 
       
     
def signin(request):
	if(request.method == 'GET'):
	   return render(request, 'crop_name_recommendation/login.html')
	else:
           if(request.method == 'POST'):
               user_name = request.POST.get('email')
               userPassword = request.POST.get('password')
               print("user Name :: ",user_name," User Password :: ",userPassword)
               users = User.objects.filter(user_email=user_name,user_password=userPassword)
               user_path = ''
               if users.count() > 0:
                  for user in users:
                     print("FOR -- user Name :: ",user_name," User Password :: ",userPassword)
                     if user.user_email==user_name and user.user_password == userPassword:
                        print("Login successfully.. ")
                        request.session['session_user_name']=user_name
                        url_path = 'crop_name_recommendation/home.html'
                        message = 'login successfully'
                     else:
                        url_path = 'crop_name_recommendation/login.html'
                        message = 'please check user name and password!!..'
               else:
                  url_path = 'crop_name_recommendation/login.html'
                  message='Please check user name and password!!...'

               template = loader.get_template(url_path)
               context = {
               'message':message,
               }
               return HttpResponse(template.render(context,request))  
      
def userLogout(request):
    try:
        del request.session['session_user_name']
        
    except KeyError:
        pass
    template = loader.get_template('crop_name_recommendation/login.html')
    context = {
               'message':'You\'re logged out.',
      }
    return HttpResponse(template.render(context,request))		


# =============================================================================
#         print("ARRAY :: ",test_records)
# =============================================================================
        #testD = ",".join(str(item) for item in test_records) 
# =============================================================================
#         print("String Test Data :: ",testD)
# =============================================================================
     
    
def svmAlgo(request): 
    if(request.method == 'POST'):
        print("request Data :: ",request.body)
        requestJson = json.loads(request.body) 
        test_records = []
        test_records.append(requestJson['soil_type'])
        test_records.append(requestJson['soil_depth'])
        test_records.append(requestJson['ph'])
        test_records.append(requestJson['bulk_density'])
        test_records.append(requestJson['ec'])
        test_records.append(requestJson['organic_carbon'])
        test_records.append(requestJson['soil_moisture_retention'])
        test_records.append(requestJson['availabel_water_capacity'])
        test_records.append(requestJson['infiltration_rate'])
        test_records.append(requestJson['clay'])
        testD = ",".join(str(item) for item in test_records) 
        svm = SVM()
        result = svm.runSVMAlgo(testD)
        response = JsonResponse({'predict_label':result})
        return response
    
def neuralNetworkAlgo(request):   
        if(request.method == 'POST'):
                print("request Data :: ",request.body)
                requestJson = json.loads(request.body) 
                test_records = []
                test_records.append(requestJson['soil_type'])
                test_records.append(requestJson['soil_depth'])
                test_records.append(requestJson['ph'])
                test_records.append(requestJson['bulk_density'])
                test_records.append(requestJson['ec'])
                test_records.append(requestJson['organic_carbon'])
                test_records.append(requestJson['soil_moisture_retention'])
                test_records.append(requestJson['availabel_water_capacity'])
                test_records.append(requestJson['infiltration_rate'])
                test_records.append(requestJson['clay'])
                testD = ",".join(str(item) for item in test_records) 
                neuralNetwork = NeuralNetwork()
                result = neuralNetwork.runAlgorithm(testD)
                response = JsonResponse({'predict_label':result})
                return response


 

def runEAlgo(request):   
        if(request.method == 'POST'):
                print("request Data :: ",request.body)
                requestJson = json.loads(request.body) 
                test_records = []
                test_records.append(requestJson['soil_type'])
                test_records.append(requestJson['soil_depth'])
                test_records.append(requestJson['ph'])
                test_records.append(requestJson['bulk_density'])
                test_records.append(requestJson['ec'])
                test_records.append(requestJson['organic_carbon'])
                test_records.append(requestJson['soil_moisture_retention'])
                test_records.append(requestJson['availabel_water_capacity'])
                test_records.append(requestJson['infiltration_rate'])
                test_records.append(requestJson['clay'])
                testD = ",".join(str(item) for item in test_records) 
                ensbl = ensemble()
                result = ensbl.runEAlgo(testD)
                response = JsonResponse({'predict_label':result})
                return response   

def fileupload(request):
   nnResult = []
   
   svmResult = []
   
   enResult = []
   if(request.method == 'POST'):
      print("request Data :: ",request.body)
      requestJson = json.loads(request.body) 
      test_records = []
      test_records.append(requestJson['soil_type'])
      test_records.append(requestJson['soil_depth'])
      test_records.append(requestJson['ph'])
      test_records.append(requestJson['bulk_density'])
      test_records.append(requestJson['ec'])
      test_records.append(requestJson['organic_carbon'])
      test_records.append(requestJson['soil_moisture_retention'])
      test_records.append(requestJson['availabel_water_capacity'])
      test_records.append(requestJson['infiltration_rate'])
      test_records.append(requestJson['clay'])
      testD = ",".join(str(item) for item in test_records) 
      neuralNetwork = NeuralNetwork()
      nnResult = neuralNetwork.runAlgorithm(testD)
      df = pd.DataFrame({"Neural ": nnResult, "SVM ":svmResult, "Ensemble":enResult})
      df.to_csv("allAlgoResult.csv", index = False)
      result = neuralNetwork.runAlgorithm(testD)
      response = JsonResponse({'predict_label':result})
      return response
   


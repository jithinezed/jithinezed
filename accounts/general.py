from pyfcm import FCMNotification
from .models import PushNotification
def push_notifier(message_title,message_body,emp_type='manager'):
    try:
        push_service = FCMNotification(api_key="AAAAu9BsO9A:APA91bEpQfOInp269wbzciZsFxMu-cRja_JlIXcNSvo1D5V1tax7FwTd8y_56ajpCL8cgKL53vFYGgKa2Hv5r2OWZhjWE-WpVD6Sj1kNkmx3wfk-EUoRPAeD6R08mJSSfKSpEK-weiTM")
        manager_list = PushNotification.objects.filter(employee__user_type=emp_type)
        print(manager_list)
        token_keys =[]
        for manager in manager_list:
            
            for keys in manager.keys.all():   
                token_keys.append(keys.key) 
        print( token_keys)        
        registration_ids = token_keys
        if len(registration_ids)>1:
            print("multiple")
            message_title = message_title
            message_body = message_body
            result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)   
            print(result)
            return result     
        if len(registration_ids)==1: 
            print("single",registration_ids[0])
            registration_id = registration_ids[0]
            message_title = message_title
            message_body = message_body
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)   
            print(result)
            return result      
    except Exception as E:
        print(str(E))
        pass  
    
def push_notifier_accounts_team(message_title,message_body,team_list):
    try:
        push_service = FCMNotification(api_key="AAAAu9BsO9A:APA91bEpQfOInp269wbzciZsFxMu-cRja_JlIXcNSvo1D5V1tax7FwTd8y_56ajpCL8cgKL53vFYGgKa2Hv5r2OWZhjWE-WpVD6Sj1kNkmx3wfk-EUoRPAeD6R08mJSSfKSpEK-weiTM")
        manager_list = []
        for i in team_list:
            print(i)
            try:
                manager_list.append(PushNotification.objects.get(employee=i))
            except:
                pass    

        print(manager_list)
        token_keys =[]
        for manager in manager_list:
            
            for keys in manager.keys.all():   
                token_keys.append(keys.key) 
        print( token_keys)        
        registration_ids = token_keys
        if len(registration_ids)>1:
            print("multiple")
            message_title = message_title
            message_body = message_body
            result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)   
            print(result)
            return result     
        if len(registration_ids)==1: 
            print("single",registration_ids[0])
            registration_id = registration_ids[0]
            message_title = message_title
            message_body = message_body
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)   
            print(result)
            return result      
    except Exception as E:
        print(str(E))
        pass 
        

def push_notifier_for_team(message_title,message_body,team_list):
    try:
        push_service = FCMNotification(api_key="AAAAu9BsO9A:APA91bEpQfOInp269wbzciZsFxMu-cRja_JlIXcNSvo1D5V1tax7FwTd8y_56ajpCL8cgKL53vFYGgKa2Hv5r2OWZhjWE-WpVD6Sj1kNkmx3wfk-EUoRPAeD6R08mJSSfKSpEK-weiTM")
        manager_list = []
        for i in team_list:
            print(i)
            try:
                manager_list.append(PushNotification.objects.get(employee=i))
            except:
                pass    

        print(manager_list)
        token_keys =[]
        for manager in manager_list:
            
            for keys in manager.keys.all():   
                token_keys.append(keys.key) 
        print( token_keys)        
        registration_ids = token_keys
        if len(registration_ids)>1:
            print("multiple")
            message_title = message_title
            message_body = message_body
            result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)   
            print(result)
            return result     
        if len(registration_ids)==1: 
            print("single",registration_ids[0])
            registration_id = registration_ids[0]
            message_title = message_title
            message_body = message_body
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)   
            print(result)
            return result      
    except Exception as E:
        print(str(E))
        pass  

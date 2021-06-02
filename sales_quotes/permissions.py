from accounts.models import Employee

def quote_permissions(profile):
    # dummy permissions
    permissions = {}
    permissions['create_quote'] = True
    
    
    try:    
            if Employee.objects.get(id=profile.id,user_type="manager"):
                permissions['create_quote'] = True

            if Employee.objects.get(id=profile.id,user_type="admin"):
                permissions['create_quote'] = True
                
            if Employee.objects.get(id=profile.id,user_type="superadmin"):
                permissions['create_quote'] = True 

            if Employee.objects.get(id=profile.id,user_type="director"):
                permissions['create_quote'] = True 
    except:
        pass

    return permissions
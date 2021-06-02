from accounts.models import Employee

# permission types

permissions_admin = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_superadmin = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_director = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_manager = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_operations_manager = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_whs_manager = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_accounts_manager = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_accounts_staff = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_accounts_staff_with_ohs = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':True,
        'intranet':True,
    }
}

permissions_pump_coordinator = {
    'companies':{
        'waste':False,
        'hills':False,
        'pumps':True,
        'destruction':False
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_scheduler = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':False,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_sales_staff = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':False,
        'vehicle':False,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_pump_technician = {
    'companies':{
        'waste':False,
        'hills':False,
        'pumps':True,
        'destruction':False
    },
    'tabs':{
        'home':True,
        'sales':False,
        'client':True,
        'team':True,
        'schedule':False,
        'vehicle':False,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_operations_assistance_manager = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':True,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_pump_manager = {
    'companies':{
        'waste':False,
        'hills':False,
        'pumps':True,
        'destruction':False
    },
    'tabs':{
        'home':True,
        'sales':True,
        'client':True,
        'team':True,
        'schedule':True,
        'vehicle':True,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_driver_liquid_waste_technician = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':False,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':False,
        'client':True,
        'team':True,
        'schedule':False,
        'vehicle':False,
        'ohs_s':False,
        'intranet':True,
    }
}

permissions_driver_factory_hand = {
    'companies':{
        'waste':True,
        'hills':True,
        'pumps':False,
        'destruction':True
    },
    'tabs':{
        'home':True,
        'sales':False,
        'client':True,
        'team':True,
        'schedule':False,
        'vehicle':False,
        'ohs_s':False,
        'intranet':True,
    }
}

all_false = {
    'companies':{
        'waste':False,
        'hills':False,
        'pumps':False,
        'destruction':False
    },
    'tabs':{
        'home':False,
        'sales':False,
        'client':False,
        'team':False,
        'schedule':False,
        'vehicle':False,
        'ohs_s':False,
        'intranet':False,
    }
}

    # admin
    # superadmin
    # director
    # manager
    # operations-manager
    # whs-manager
    # accounts-manager
    # accounts-staff
    # pump-coordinator
    # scheduler
    # sales-staff
    # pump-technician
    # operations-assistance-manager
    # pump-manager
    # driver-liquid-waste-technician
    # driver-factory-hand

def get_permissions(user_type):  
    if user_type =='admin':
        return permissions_admin

    elif user_type =='superadmin':
        return permissions_superadmin
    
    elif user_type =='director':
        return permissions_director
    
    elif user_type =='manager':
        return permissions_manager
    
    elif user_type =='operations-manager':
        return permissions_operations_manager
    
    elif user_type =='whs-manager':
        return permissions_whs_manager
    
    elif user_type =='accounts-manager':
        return permissions_accounts_manager
    
    elif user_type =='accounts-staff':
        return permissions_accounts_staff
    
    elif user_type =='pump-coordinator':
        return permissions_pump_coordinator
    
    elif user_type =='scheduler':
        return permissions_scheduler
    
    elif user_type =='sales-staff':
        return permissions_sales_staff
    
    elif user_type =='pump-technician':
        return permissions_pump_technician
    
    elif user_type =='operations-assistance-manager':
        return permissions_operations_assistance_manager
    
    elif user_type =='pump-manager':
        return permissions_pump_manager
    
    elif user_type =='driver-liquid-waste-technician':
        return permissions_driver_liquid_waste_technician
    
    elif user_type =='driver-factory-hand':
        return permissions_driver_factory_hand
    
    else:
        return all_false

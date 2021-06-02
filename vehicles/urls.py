from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('all/<str:v_type>/', views.getAllVehicleAPI, name='getAllVehicleAPI'),
    path('all/<str:v_type>/<int:page_number>/', views.getAllVehicleAPI, name='getAllVehicleAPI'),

    path('create/', views.vehicleCreateAPI, name='vehicleCreateAPI'),   
    path('delete/<str:vehicle_id>/', views.vehicleDeleteAPI, name='vehicleDeleteAPI'),
    path('edit/<str:vehicle_id>/', views.vehicleEditAPI, name='vehicleEditAPI'),
    path('fleet/list/<int:vehicle_id>/', views.getAllFleet, name='getAllFleet'),
    path('fleet/list/<int:vehicle_id>/<int:page_number>/', views.getAllFleet, name='getAllFleet'), 
    path('FleetCreate/', views.fleetCreateAPI, name='fleetCreateAPI'),  
    path('deleteFleet/<str:fleet_id>/', views.fleetDeleteAPI, name='fleetDeleteAPI'), 
    path('editFleet/<str:fleet_id>/', views.fleetEditAPI, name='fleetEditAPI'),
    path('maintenance/report/truck/create/', views.maintananceReportCreateAPI, name='maintananceReportCreateAPI'),
    path('maintenance/reports/truck/', views.getMaintananceReports, name='getMaintananceReports'),
    path('maintenance/reports/truck/<int:page_number>/', views.getMaintananceReports, name='getMaintananceReports'),

    path('maintenance/report/truck/edit/<str:reportId>/', views.ReportEditAPI, name='ReportEditAPI'),
    path('maintenance/report/truck/delete/<str:report_id>/', views.MaintananceReportDelete, name='MaintananceReportDelete'),
    path('maintenace/reports/truck/search/', views.searchReport, name='searchReport'),
    path('maintenace/reports/truck/search/<int:page_number>/', views.searchReport, name='searchReport'),
    path('maintenace/reports/truck/search/<str:filter_type>/', views.truck_maintanance_search_by, name='truck_maintanance_search_by'),
   
    path('maintenance/report/car/create/', views.carmaintananceReportCreateAPI, name='carmaintananceReportCreateAPI'),
    path('maintenance/reports/car/', views.getCarMaintananceReports, name='getCarMaintananceReports'),
    path('maintenance/reports/car/<int:page_number>/', views.getCarMaintananceReports, name='getCarMaintananceReports'),
   

    path('maintenance/report/car/edit/<str:reportId>/', views.getCarMaintananceReports, name='getCarMaintananceReports'),
    path('maintenance/report/car/delete/<str:reportId>/', views.getCarMaintananceReports, name='MaintananceReportDelete'),
    path('maintenace/reports/car/search/', views.car_searchReport, name='car_searchReport'),
    path('maintenace/reports/car/search/<int:page_number>/', views.car_searchReport, name='car_searchReport'),
    path('maintenance/reports/car/search/<str:filter_type>/', views.car_maintanance_search_by, name='car_maintanance_search_by'),
    path('addFuelExpense/', views.addFuelExpense, name='addFuelExpense'),
    path('getFuelExpenses/<str:v_type>/', views.getFuelExpense, name='getFuelExpense'),
    path('getFuelExpenses/<str:v_type>/<int:page_number>/', views.getFuelExpense, name='getFuelExpense'),
    path('deleteFuelExpense/<str:fuelEXP_id>/', views.FuelExpenseDelete, name='FuelExpenseDelete'),
    path('editFuelExpense/<str:fuelEXP_id>/', views.fuelExpenseEditAPI, name='fuelExpenseEditAPI'),
    path('fuelExpense/search/<str:filter_type>/', views.fuel_expns_search_by, name='fuel_expns_search_by'),
    path('vehicle/id/<str:v_type>/', views.getAllvehicleId, name='getAllvehicleId'),
    path('forklift/maintenance/report/create/', views.forkLiftMaintananceReportCreateAPI, name='forkLiftMaintananceReportCreateAPI'),
    path('forklift/maintenance/reports/', views.getForkliftMaintananceReports, name='getForkliftMaintananceReports'),
    path('forklift/maintenance/reports/<int:page_number>/', views.getForkliftMaintananceReports, name='getForkliftMaintananceReports'),
    path('forklift/maintenance/edit/<str:reportId>/', views.ForlliftReportEditAPI, name='ForlliftReportEditAPI'),
    path('forklift/maintanace/report/delete/<str:report_id>/', views.ForkliftMaintananceReportDelete, name='ForkliftMaintananceReportDelete'),
    path('forklift/maintenance-reports/search/', views.forkliftSearchReport, name='forkliftSearchReport'),
    path('forklift/maintenance-reports/search/<int:page_number>/', views.forkliftSearchReport, name='forkliftSearchReport'),
    path('forklift/maintenance-reports/search/<str:filter_type>/', views.lift_maintanance_search_by, name='lift_maintanance_search_by'),
    path('pre-inspection/<str:v_type>/',views.getAllPreInspection,name='getAllPreInspection'),
    path('pre-inspection/<str:v_type>/<int:page_number>/',views.getAllPreInspection,name='getAllPreInspection'),
  
    path('pre_inspection/edit/<int:check_id>/',views.PreInspectionEidt,name='PreInspectionEidt'),
   
    path('inspection/<str:v_type>/<int:check_id>/',views.getPreInspectionById,name='getPreInspectionById'),
    path('inspection/<str:v_type>/<int:check_id>/<int:page_number>/',views.getPreInspectionById,name='getPreInspectionById'),
    path('pre-inspection/filter/<str:filter_type>/',views.pre_ins_search_by,name='pre_ins_search_by'),
  

    path('files/upload/<int:vehicle_id>/', views.folders, name='folders'),
    path('files/<int:vehicle_id>/', views.getVehicleFolders, name='getVehicleFolders'),


    path('search/', views.vehicle_search, name='vehicle_search'),

    path('search/<int:page_number>/', views.vehicle_search, name='vehicle_search'),

    path('folder/list/', views.get_all_VehicleFolders, name='get_all_VehicleFolders'),



    path('file/delete/<int:file_id>/', views.delete_vehicle_files, name='delete_vehicle_files'),  

    path('update/<str:f_type>/create/', views.update_team_folder, name='update_team_folder'),
    path('update/<str:f_type>/<int:f_id>/', views.update_team_folder, name='update_team_folder'),
    path('update/images/list/<int:vehicle_id>/', views.vehicle_multiple_images_update, name='vehicle_multiple_images_update'),

]



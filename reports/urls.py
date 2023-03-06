from django.urls import path
from .views import *


urlpatterns = [
    path("list", get_report_list, name='report-list'),
    path("status", get_statatics, name='view-status'),
    path('monthly/child_labour', upload_child_labour, name='child-labour'),
    path('monthly/child_marriage', upload_child_marriage, name='child-marriage'),
    path('monthly/saranabalyam', upload_sarana_balyam, name='sarana-balyam'),
    path('monthly/violence_against_children', upload_children_violance, name='violence-against-children'),
    path('monthly/parenting_outreach', parenting_outreach, name='parenting-outreach'),
    path('monthly/parenting_clinic', parenting_clinic, name='parenting-clinic'),
    #admin
    path("monthly/<str:month>/<str:year>/admin_saranabalyam", admin_sarana_balyam, name="admin_saranabalyam"),
    path("monthly/<str:month>/<str:year>/admin_parenting_outreach", admin_parenting_outreach, name="admin_parenting_outreach"),
    path("monthly/<str:month>/<str:year>/admin_parenting_clinic", admin_parenting_clinic, name="admin_parenting_clinic"),

    # quarterly
    path('quarterly/state_sponsership', upload_state_sponsership, name='state-sponsership'),
    path('quarterly/central_sponsership', upload_central_sponsership, name='central-sponsership'),
    path('quarterly/after_care_service', upload_after_care_service, name="after-care-service"),
    path('quarterly/after_care_children_cci', upload_after_care_children_cci, name="after-care-children-cci"),
    path('quarterly/crime_committed', upload_crime_committed_children , name="crime-committed-children"),
    path('quarterly/juvenile_justice', upload_juvenile_justice, name="juvenile-justice"),
    path('quarterly/jja', upload_jja, name="jja"),
    path('quarterly/pocso', upload_pocso, name="pocso"),
    path('quarterly/deinstitutional', upload_deinstitutional, name="deinstitutional"),
    path('quarterly/jjb', upload_jjb, name="jjb"),
    path('quarterly/institutional_care', upload_institutional_care, name="institutional_care"),
    path('quarterly/cwc', upload_casescwc, name="cwc"),
    path('quarterly/institutional_care_protection', upload_institutional_care_protection, name="institutional-care-protection"),
    path('quarterly/adoption', upload_adoption, name="adoption"),
    path('quarterly/child_protection', upload_child_protection, name="child-protection"),
    path('quarterly/foster_care', upload_foster_care, name="foster-care"),
    path('quarterly/repatriation', upload_repatriation, name="repatriation"),
    path('quarterly/ncpcr', upload_ncpcr, name="ncpcr"),
    path('quarterly/qprsc', upload_qprsc, name="qprsc"),
    path('quarterly/qprhc', upload_qprhc, name="qprhc"),
    #admin
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_ncpcr", admin_ncpcr, name="admin-ncpcr"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_centralsponsorship", admin_centralsponsorship, name="admin-centralsponsorship"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_aftercareservices", admin_aftercareservices, name="admin-aftercareservices"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_aftercarecci", admin_aftercarecci, name="admin-aftercarecci"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_crimecommitted", admin_crimecommitted, name="admin-crimecommitted"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_qprsc", admin_qprsc, name="admin-qprsc"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_qprhc", admin_qprhc, name="admin-qprhc"),
    path("monthly/<str:month>/<str:year>/admin_cm" , admin_childmarriage, name="admin_childmarriage"),
    path("monthly/<str:month>/<str:year>/admin_childlabour", admin_childlabour, name="admin_childlabour"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_cwc", admin_cwc, name="admin_cwc"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_fostercare", admin_fostercare, name="admin_fostercare"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_repatriation", admin_repatriation, name="admin_repatriation"),
    path("quarterly/<str:Qmonth>/<str:Qyear>/admin_violence_against_children", admin_violence, name="admin_violence"),
    # yearly
    path("yearly/resource_person", upload_resource_person, name="resource-person"),
    path("yearly/<str:annually>/admin_resource_person", admin_resource_person, name="admin-resource_person")

    
]
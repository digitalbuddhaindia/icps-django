from datetime import datetime
from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from accounts.permissions import IsDistrictUser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models.functions import ExtractQuarter
from django.contrib.auth import get_user_model
from .serializers import *
from .models import ReportCategory, ReportType
from django.db.models import Count,Case,When,IntegerField
from django.db.models import Sum
from django.http import JsonResponse
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_list(request):
    reports = ReportType.objects.all()
    serializer = ReportCategorySerializer(reports, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsDistrictUser])
def get_statatics(request):
    today = datetime.now()
    year = today.year
    month = today.month
    quarter = (month - 1)//3+1
    user = request.user
    submitted=ReportType.objects.aggregate(total=Count(Case(
        When(childlabour__created_at__year=year,childlabour__created_at__month=month, childlabour__user=user, then=1),
        When(childmarriage__created_at__year=year, childmarriage__created_at__month=month,childmarriage__user=user, then=1),
        When(saranabalyam__created_at__year=year, saranabalyam__created_at__month=month,saranabalyam__user=user, then=1),
        When(statesponsorship__created_at__year=year, statesponsorship__created_at__quarter=quarter,statesponsorship__user=user, then=1),
        When(centralsponsorship__created_at__year=year, centralsponsorship__created_at__quarter=quarter,centralsponsorship__user=user, then=1),
        When(aftercareservice__created_at__year=year, aftercareservice__created_at__quarter=quarter,aftercareservice__user=user, then=1),
        When(aftercarechildrencci__created_at__year=year, aftercarechildrencci__created_at__quarter=quarter,aftercarechildrencci__user=user, then=1),
        When(crimecommittedchildren__created_at__year=year, crimecommittedchildren__created_at__quarter=quarter,crimecommittedchildren__user=user, then=1),
        When(juvenilejustice__created_at__year=year, juvenilejustice__created_at__quarter=quarter,juvenilejustice__user=user, then=1),
        When(jja__created_at__year=year, jja__created_at__quarter=quarter,jja__user=user, then=1),
        When(pocso__created_at__year=year, pocso__created_at__quarter=quarter,pocso__user=user, then=1),
        When(deinstitutional__created_at__year=year, deinstitutional__created_at__quarter=quarter,deinstitutional__user=user, then=1),
        When(jjb__created_at__year=year, jjb__created_at__quarter=quarter,jjb__user=user, then=1),
        When(institutionalcare__created_at__year=year, institutionalcare__created_at__quarter=quarter,institutionalcare__user=user, then=1),
        When(cwc__created_at__year=year, cwc__created_at__quarter=quarter,cwc__user=user, then=1),
        When(institutionalcareprotection__created_at__year=year, institutionalcareprotection__created_at__quarter=quarter,institutionalcareprotection__user=user, then=1),
        When(adoption__created_at__year=year, adoption__created_at__quarter=quarter,adoption__user=user, then=1),
        When(childprotection__created_at__year=year, childprotection__created_at__quarter=quarter,childprotection__user=user, then=1),
        When(fostercare__created_at__year=year, fostercare__created_at__quarter=quarter,fostercare__user=user, then=1),
        When(repatriation__created_at__year=year, repatriation__created_at__quarter=quarter,repatriation__user=user, then=1),
        When(resourceperson__created_at__year=year,resourceperson__user=user,then=1),
        output_field=IntegerField(),)))
    return Response({'total': 36, "submitted":submitted['total'],'pending':36 - submitted['total']})
    

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_child_labour(request):
    if request.method == 'POST':
        user = request.user
        report_type = ReportType.objects.get(id=2)
        serializer = ChildLabourSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            check_previous = ChildLabour.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ChildLabourSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ChildLabour.objects.filter(user=request.user)
        serializer = ChildLabourSerializer(data, many=True)
        return Response(serializer.data)
    

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_child_marriage(request):
    if request.method == 'POST':
        serializer = ChildMarriageSerializer(data=request.data)
        if serializer.is_valid():
            data=request.data
            created_at = datetime.now()
            user = request.user
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=1)
            check_previous = ChildMarriage.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ChildMarriageSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)   
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ChildMarriage.objects.filter(user=request.user)
        serializer = ChildMarriageSerializer(data, many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_sarana_balyam(request):
    if request.method == 'POST':
        serializer = SaranabalyamSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            data=request.data
            year = data['year']
            month =  data['month']
            user = request.user
            username = request.user.username
            report_type = ReportType.objects.get(id=3)
            check_previous = Saranabalyam.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username, year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = SaranabalyamSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = Saranabalyam.objects.filter(user=request.user)
        serializer = SaranabalyamSerializer(data, many=True)
        return Response(serializer.data)

       
        
    

# @api_view(['POST', 'GET'])
# @permission_classes([IsDistrictUser])
# def upload_sarana_balyam(request,pk):
#     if request.method == 'POST':
#         

#         if serializer.is_valid():
#             created_at = datetime.now()
#             user = request.user
#             try:
#                 report_type = ReportType.objects.get(id=pk,report_category__name="Saranabalyam")
#             except:
#                 response = {
#                     "message": "not a saranabalyam category",
#                 }
#                 return Response(response, status=status.HTTP_400_BAD_REQUEST)
#             check_previous = Saranabalyam.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
#             if check_previous:
#                 check_previous.created_at = created_at
#                 serializer = SaranabalyamSerializer(check_previous, data=request.data)
#                 if serializer.is_valid():
#                     serializer.save(created_at=created_at, user=user, report_type=report_type)
#                     return Response(serializer.data, status=status.HTTP_200_OK)
                
#             serializer.save(created_at=created_at, user=user, report_type=report_type)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         data = Saranabalyam.objects.filter(user=request.user, report_type__id=pk)
#         serializer = SaranabalyamSerializer(data, many=True)
#         return Response(serializer.data)
        
    
# @api_view(['POST', 'GET'])
# @permission_classes([IsDistrictUser])
# def upload_children_violance(request,pk):
#     if request.method == 'POST':
#         serializer = ChildrenViolenceSerializer(data=request.data)
#         if serializer.is_valid():
#             created_at = datetime.now()
#             user = request.user
#             try:
#                 report_type = ReportType.objects.get(id=pk,report_category__name="Violence against Children")
#             except:
#                 response = {
#                     "message": "not violence against children category",
#                 }
#                 return Response(response, status=status.HTTP_400_BAD_REQUEST)
#             check_previous = ChildrenViolence.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
#             if check_previous:
#                 check_previous.created_at = created_at
#                 serializer = ChildrenViolenceSerializer(check_previous, data=request.data)
#                 if serializer.is_valid():
#                     serializer.save(created_at=created_at, user=user, report_type=report_type)
#                     return Response(serializer.data, status=status.HTTP_200_OK)

#             serializer.save(created_at=created_at, user=user, report_type=report_type)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         data = ChildrenViolence.objects.filter(user=request.user, report_type__id=pk)
#         serializer = ChildrenViolenceSerializer(data, many=True)
#         return response(serializer.data)



@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_children_violance(request):
    if request.method == 'POST':
        serializer = ChildrenViolenceSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=40)
            check_previous = ChildrenViolence.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ChildrenViolenceSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ChildrenViolence.objects.filter(user=request.user)
        serializer = ChildrenViolenceSerializer(data, many=True)
        return Response(serializer.data)
        
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def parenting_outreach(request):
    if request.method == 'POST':
        serializer = ParentingOutreachSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=41)
            check_previous = ParentingOutreach.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ParentingOutreachSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ParentingOutreach.objects.filter(user=request.user)
        serializer = ParentingOutreachSerializer(data, many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def parenting_clinic(request):
    if request.method == 'POST':
        serializer = ParentingClinicSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=42)
            check_previous = ParentingClinic.objects.filter(created_at__month=created_at.month,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ParentingClinicSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ParentingClinic.objects.filter(user=request.user)
        serializer = ParentingClinicSerializer(data, many=True)
        return Response(serializer.data)


@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_state_sponsership(request):
    if request.method == 'POST':
        serializer = StateSponsershipSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=19)
            quarter_value=(created_at.month-1)//3+1
            check_previous = StateSponsorship.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = StateSponsershipSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data =  StateSponsorship.objects.filter(user=request.user)
        serializer = StateSponsershipSerializer(data, many=True)
        return Response(serializer.data)
        

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_central_sponsership(request):
    if request.method == 'POST':
        serializer = CentralSponsershipSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            username = request.user.username
            data=request.data
            year = data['year']
            month =  data['month']
            report_type = ReportType.objects.get(id=20)
            quarter_value=(created_at.month-1)//3+1
            check_previous = CentralSponsorship.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = CentralSponsershipSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = CentralSponsorship.objects.filter(user=request.user)
        serializer = CentralSponsershipSerializer(data, many=True)
        return Response(serializer.data)
        

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_after_care_service(request):
    if request.method == 'POST':
        serializer = AfterCareServiceSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            username = request.user.username
            data=request.data
            year = data['year']
            month =  data['month']
            report_type = ReportType.objects.get(id=21)
            quarter_value=(created_at.month-1)//3+1
            check_previous = AfterCareService.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,username=username,report_type=report_type,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = AfterCareServiceSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = AfterCareService.objects.filter(user=request.user)
        serializer = AfterCareServiceSerializer(data, many=True)
        return Response(serializer.data)
        

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_after_care_children_cci(request):
    if request.method == 'POST':
        serializer = AfterCareChildrenCciSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            username = request.user.username
            data=request.data
            year = data['year']
            month =  data['month']
            report_type = ReportType.objects.get(id=22)
            quarter_value=(created_at.month-1)//3+1
            check_previous = AfterCareChildrenCci.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,username=username,report_type=report_type,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = AfterCareChildrenCciSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':    
        data = AfterCareChildrenCci.objects.filter(user=request.user)
        serializer = AfterCareChildrenCciSerializer(data, many=True)
        return Response(serializer.data)
        

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_crime_committed_children(request):
    if request.method == 'POST':
        serializer = CrimeCommittedChildrenSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=23)
            quarter_value=(created_at.month-1)//3+1
            check_previous = CrimeCommittedChildren.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = CrimeCommittedChildrenSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = CrimeCommittedChildren.objects.filter(user=request.user)
        serializer = CrimeCommittedChildrenSerializer(data, many=True)
        return Response(serializer.data)
    
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_juvenile_justice(request):
    if request.method == 'POST':
        serializer = JuvenileJusticeserializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=24)
            quarter_value=(created_at.month-1)//3+1
            check_previous = JuvenileJustice.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = JuvenileJusticeserializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':   
        data = JuvenileJustice.objects.filter(user=request.user)
        serializer = JuvenileJusticeserializer(data, many=True)
        return Response(serializer.data)
    
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_jja(request):
    if request.method == 'POST':
        serializer = JjaSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=25)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Jja.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = JjaSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = Jja.objects.filter(user=request.user)
        serializer = JjaSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_pocso(request):
    if request.method == 'POST':
        serializer = PocsoSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=26)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Pocso.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = PocsoSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = Pocso.objects.filter(user=request.user)
        serializer = PocsoSerializer(data, many=True)
        return Response(serializer.data)
        
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_casescwc(request):
    if request.method == 'POST':
        serializer = CasesCwcSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            report_type = ReportType.objects.get(id=30)
            username =request.user.username
            quarter_value=(created_at.month-1)//3+1
            check_previous = CasesCwc.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username ,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = CasesCwcSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = CasesCwc.objects.filter(user=request.user)
        serializer = CasesCwcSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_deinstitutional(request):
    if request.method == 'POST':
        serializer = DeInstitutionalSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=27)
            quarter_value=(created_at.month-1)//3+1
            check_previous = DeInstitutional.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = DeInstitutionalSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = DeInstitutional.objects.filter(user=request.user)
        serializer = DeInstitutionalSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_jjb(request):
    if request.method == 'POST':
        serializer = JjbSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=28)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Jjb.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = JjbSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = Jjb.objects.filter(user=request.user)
        serializer = JjbSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_institutional_care(request):
    if request.method == 'POST':
        serializer = InstitutionalCareSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=29)
            quarter_value=(created_at.month-1)//3+1
            check_previous = InstitutionalCare.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = InstitutionalCareSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = InstitutionalCare.objects.filter(user=request.user)
        serializer = InstitutionalCareSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_cwc(request):
    if request.method == 'POST':
        serializer = CwcSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            report_type = ReportType.objects.get(id=30)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Cwc.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = CwcSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = Cwc.objects.filter(user=request.user)
        serializer = CwcSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_institutional_care_protection(request):
    if request.method == 'POST':
        serializer = InstitutionalCareProtectionSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=31)
            quarter_value=(created_at.month-1)//3+1
            check_previous = InstitutionalCareProtection.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = InstitutionalCareProtectionSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = InstitutionalCareProtection.objects.filter(user=request.user)
        serializer = InstitutionalCareProtectionSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_adoption(request):
    if request.method == 'POST':
        serializer = AdoptionSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=32)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Adoption.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = AdoptionSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = Adoption.objects.filter(user=request.user)
        serializer = AdoptionSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_child_protection(request):
    if request.method == 'POST':
        serializer = ChildProtectionSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            report_type = ReportType.objects.get(id=33)
            quarter_value=(created_at.month-1)//3+1
            check_previous = ChildProtection.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ChildProtectionSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = ChildProtection.objects.filter(user=request.user)
        serializer = ChildProtectionSerializer(data, many=True)
        return Response(serializer.data)
        

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_foster_care(request):
    if request.method == 'POST':
        serializer = FosterCareSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=34)
            quarter_value=(created_at.month-1)//3+1
            check_previous = FosterCare.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = FosterCareSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = FosterCare.objects.filter(user=request.user)
        serializer = FosterCareSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_repatriation(request):
    if request.method == 'POST':
        serializer = RepatriationSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=35)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Repatriation.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = RepatriationSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = Repatriation.objects.filter(user=request.user)
        serializer = RepatriationSerializer(data, many=True)
        return Response(serializer.data)
        
    
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_resource_person(request):
    if request.method == 'POST':
        serializer = ResourcePersonSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            report_type = ReportType.objects.get(id=36)
            username = request.user.username
            check_previous = ResourcePerson.objects.filter(created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = ResourcePersonSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':   
        data = ResourcePerson.objects.filter(user=request.user)
        serializer = ResourcePersonSerializer(data, many=True)
        return Response(serializer.data)
        
 
@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_ncpcr(request):
    if request.method == 'POST':
        serializer = NcpcrSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            username = request.user.username
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            report_type = ReportType.objects.get(id=37)
            quarter_value=(created_at.month-1)//3+1
            check_previous = Ncpcr.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = NcpcrSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':   
        data = Ncpcr.objects.filter(user=request.user)
        serializer = NcpcrSerializer(data, many=True)
        return Response(serializer.data)  

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_qprsc(request):
    if request.method == 'POST':
        serializer = QprscSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=38)
            quarter_value=(created_at.month-1)//3+1
            check_previous = QprSupremeCourt.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = QprscSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':   
        data = QprSupremeCourt.objects.filter(user=request.user)
        serializer = QprscSerializer(data, many=True)
        return Response(serializer.data) 

@api_view(['POST', 'GET'])
@permission_classes([IsDistrictUser])
def upload_qprhc(request):
    if request.method == 'POST':
        serializer = QprhcSerializer(data=request.data)
        if serializer.is_valid():
            created_at = datetime.now()
            user = request.user
            data=request.data
            year = data['year']
            month =  data['month']
            username = request.user.username
            report_type = ReportType.objects.get(id=39)
            quarter_value=(created_at.month-1)//3+1
            check_previous = QprHighCourt.objects.filter(created_at__quarter=quarter_value,created_at__year=created_at.year,user=request.user,report_type=report_type,username=username,year=year,month=month).last()
            if check_previous:
                check_previous.created_at = created_at
                serializer = QprhcSerializer(check_previous, data=request.data)
                if serializer.is_valid():
                    serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(created_at=created_at, user=user, report_type=report_type,username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':   
        data = QprHighCourt.objects.filter(user=request.user)
        serializer = QprhcSerializer(data, many=True)
        return Response(serializer.data)


#admin
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_sarana_balyam(request,year,month):
    if request.method == 'POST':
        serializer = SaranabalyamSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = Saranabalyam.objects.filter(month=month , year = year)
        serializer = SaranabalyamSerializer(data,many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_ncpcr(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = NcpcrSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = Ncpcr.objects.filter(month=Qmonth , year = Qyear)
        serializer = NcpcrSerializer(data,many=True)
        # fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
        #      '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
        #      '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
        #      '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
        #      '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
        #      '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
        #      '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
        #      '_check_model_name_db_lookup_clashes', '_check_ordering',
        #      '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
        #      '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
        #      'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
        #      'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
        #      '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
        #      '_save_table', '_set_pk_val', '_state', 'id']
        # response_dict = {}
        # for i in data:
            
        #     for j in dir(i):
        #         if j not in fields:
        #             p = getattr(i, str(j))
        #             if isinstance(p, int):
        #                 if 'sum_'+j in response_dict:
        #                     response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
        #                 else:
        #                     response_dict['sum_' + j] = getattr(i, str(j))
        return Response(serializer.data)
#admin
#centralsponsorship
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_centralsponsorship(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = CentralSponsershipSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = CentralSponsorship.objects.filter( year = Qyear)
        serializer = CentralSponsershipSerializer(data,many=True)
        return Response(serializer.data)

#aftercareservices
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_aftercareservices(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = AfterCareServiceSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = AfterCareService.objects.filter( year = Qyear)
        serializer = AfterCareServiceSerializer(data,many=True)
        return Response(serializer.data)

#aftercarecci
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_aftercarecci(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = AfterCareChildrenCciSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = AfterCareChildrenCci.objects.filter( year = Qyear)
        serializer = AfterCareChildrenCciSerializer(data,many=True)
        return Response(serializer.data)

#crimecommitted
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_crimecommitted(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = CrimeCommittedChildrenSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = CrimeCommittedChildren.objects.filter( year = Qyear)
        fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
             '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
             '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
             '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
             '_check_model_name_db_lookup_clashes', '_check_ordering',
             '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
             '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
             'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
             'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
             '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
             '_save_table', '_set_pk_val', '_state', 'id']
        response_dict = {}
        serializer = CrimeCommittedChildrenSerializer(data,many=True)
        for i in data:

            for j in dir(i):
                if j not in fields:
                    p = getattr(i, str(j))
                    if isinstance(p, int):
                        if 'sum_'+j in response_dict:
                            response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
                        else:
                            response_dict['sum_' + j] = getattr(i, str(j))
        return Response(serializer.data)

#admin_resource_person
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_resource_person(request,annually):
    if request.method == 'POST':
        serializer = ResourcePersonSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ResourcePerson.objects.filter(year=annually)
        serializer = ResourcePersonSerializer(data,many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_qprsc(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = QprscSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = QprSupremeCourt.objects.filter(month=Qmonth , year = Qyear)
        serializer = QprscSerializer(data,many=True)
        fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
             '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
             '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
             '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
             '_check_model_name_db_lookup_clashes', '_check_ordering',
             '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
             '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
             'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
             'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
             '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
             '_save_table', '_set_pk_val', '_state', 'id']
        response_dict = {}
        for i in data:

            for j in dir(i):
                if j not in fields:
                    p = getattr(i, str(j))
                    if isinstance(p, int):
                        if 'sum_'+j in response_dict:
                            response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
                        else:
                            response_dict['sum_' + j] = getattr(i, str(j))
        return Response(response_dict)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_qprhc(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = QprhcSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = QprHighCourt.objects.filter(month=Qmonth , year = Qyear)
        fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
             '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
             '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
             '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
             '_check_model_name_db_lookup_clashes', '_check_ordering',
             '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
             '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
             'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
             'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
             '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
             '_save_table', '_set_pk_val', '_state', 'id']
        response_dict = {}
        serializer = QprhcSerializer(data,many=True)
        for i in data:

            for j in dir(i):
                if j not in fields:
                    p = getattr(i, str(j))
                    if isinstance(p, int):
                        if 'sum_'+j in response_dict:
                            response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
                        else:
                            response_dict['sum_' + j] = getattr(i, str(j))
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_childmarriage(request,year,month):
    if request.method == 'POST':
        serializer = ChildMarriageSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ChildMarriage.objects.filter(month=month , year = year)
        serializer = ChildMarriageSerializer(data,many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_childlabour(request,year,month):
    if request.method == 'POST':
        serializer = ChildLabourSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ChildLabour.objects.filter(month=month , year = year)
        serializer = ChildLabourSerializer(data,many=True)
        # fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
        #      '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
        #      '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
        #      '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
        #      '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
        #      '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
        #      '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
        #      '_check_model_name_db_lookup_clashes', '_check_ordering',
        #      '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
        #      '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
        #      'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
        #      'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
        #      '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
        #      '_save_table', '_set_pk_val', '_state', 'id']
        # response_dict = {}
        # for i in data:
        #     for j in dir(i):
        #         if j not in fields:
        #             p = getattr(i, str(j))
        #             if isinstance(p, int):
        #                 if 'sum_'+j in response_dict:
        #                     response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
        #                 else:
        #                     response_dict['sum_' + j] = getattr(i, str(j))
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_cwc(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = CasesCwcSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = CasesCwc.objects.filter( year = Qyear)
        serializer = CasesCwcSerializer(data,many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_fostercare(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = FosterCareSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = FosterCare.objects.filter( year = Qyear)
        fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
             '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
             '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
             '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
             '_check_model_name_db_lookup_clashes', '_check_ordering',
             '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
             '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
             'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
             'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
             '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
             '_save_table', '_set_pk_val', '_state', 'id']
        response_dict = {}
        serializer = FosterCareSerializer(data,many=True)
        for i in data:

            for j in dir(i):
                if j not in fields:
                    p = getattr(i, str(j))
                    if isinstance(p, int):
                        if 'sum_'+j in response_dict:
                            response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
                        else:
                            response_dict['sum_' + j] = getattr(i, str(j))
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_repatriation(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = RepatriationSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = Repatriation.objects.filter(month=Qmonth , year = Qyear)
        fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
             '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
             '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
             '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
             '_check_model_name_db_lookup_clashes', '_check_ordering',
             '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
             '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
             'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
             'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
             '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
             '_save_table', '_set_pk_val', '_state', 'id']
        response_dict = {}
        serializer = RepatriationSerializer(data,many=True)
        for i in data:

            for j in dir(i):
                if j not in fields:
                    p = getattr(i, str(j))
                    if isinstance(p, int):
                        if 'sum_'+j in response_dict:
                            response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
                        else:
                            response_dict['sum_' + j] = getattr(i, str(j))
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_violence(request,Qmonth,Qyear):
    if request.method == 'POST':
        serializer = ChildrenViolenceSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ChildrenViolence.objects.filter(month=Qmonth , year = Qyear)
        serializer = ChildrenViolenceSerializer(data,many=True)
        fields = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
             '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
             '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
             '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
             '_check_model_name_db_lookup_clashes', '_check_ordering',
             '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable',
             '_check_unique_together', '_do_insert', '_doing_sensitisation_to_jjb_has_been_provided', 'updated_at',
             'user', 'user_id', 'validate_unique', 'name', 'report_type', 'report_type_id', 'objects',
             'unique_error_message', 'prepare_database_save', 'pk', 'clean_fields', 'clean', 'check',
             '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents',
             '_save_table', '_set_pk_val', '_state', 'id']
        response_dict = {}
        for i in data:

            for j in dir(i):
                if j not in fields:
                    p = getattr(i, str(j))
                    if isinstance(p, int):
                        if 'sum_'+j in response_dict:
                            response_dict['sum_'+j] = response_dict['sum_'+j] + getattr(i, str(j))
                        else:
                            response_dict['sum_' + j] = getattr(i, str(j))
        return Response(response_dict)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_parenting_outreach(request,year,month):
    if request.method == 'POST':
        serializer = ParentingOutreachSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ParentingOutreach.objects.filter( year = year)
        serializer = ParentingOutreachSerializer(data,many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def admin_parenting_clinic(request,year,month):
    if request.method == 'POST':
        serializer = ParentingClinicSerializer(many=True)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        data = ParentingClinic.objects.filter(  year = year)
        serializer = ParentingClinicSerializer(data,many=True)
        return Response(serializer.data)
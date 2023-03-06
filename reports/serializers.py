from pickle import TRUE
from rest_framework import serializers
from .models import *


class ReportCategorySerializer(serializers.ModelSerializer):
    category  = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = ReportType
        fields = ('id','name', 'category', 'type')
        
    def get_category(self, obj):
        category = obj.report_category.name
        return category
    
    def get_type(self, obj):
        type = obj.report_category.category
        return type
    
    
class ReportSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('user','report_type','response','created_at')
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}}
        
        

class ChildLabourSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChildLabour
        fields = '__all__'
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
class ParentingOutreachSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParentingOutreach
        fields = '__all__'
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}

class ParentingClinicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParentingClinic
        fields = '__all__'
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}

class ChildMarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMarriage
        fields = '__all__'
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class SaranabalyamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saranabalyam
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class ChildrenViolenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildrenViolence
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class StateSponsershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateSponsorship
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
class CentralSponsershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentralSponsorship
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class AfterCareServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfterCareService
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class AfterCareChildrenCciSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfterCareChildrenCci
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class CrimeCommittedChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeCommittedChildren
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class JuvenileJusticeserializer(serializers.ModelSerializer):
    class Meta:
        model = JuvenileJustice
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class JjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jja
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class PocsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pocso
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class CasesCwcSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasesCwc
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
              
class DeInstitutionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeInstitutional
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class JjbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jjb
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class InstitutionalCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionalCare
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        

class CwcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cwc
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class InstitutionalCareProtectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionalCareProtection 
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class ChildProtectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProtection
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class FosterCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = FosterCare
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class RepatriationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repatriation
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
        
        
class ResourcePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourcePerson
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}


class NcpcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ncpcr
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}

class QprscSerializer(serializers.ModelSerializer):
    class Meta:
        model = QprSupremeCourt
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}

class QprhcSerializer(serializers.ModelSerializer):
    class Meta:
        model = QprHighCourt
        fields = "__all__"
        extra_kwargs = {'created_at': {'required':False}, 'user':{'required':False}, 'report_type': {'required':False}}
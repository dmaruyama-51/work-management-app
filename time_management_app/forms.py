from django import forms 
from time_management_app.models import TimeManagement 

class TimeManagementForm(forms.ModelForm):
    class Meta:
        model = TimeManagement
        fields = ('date', 'start_time', 'end_time', 'rest_time', 'travel_cost', 'travel_remarks', 'rating', 'comment')
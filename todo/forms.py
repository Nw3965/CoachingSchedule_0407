from django import forms
from todo.models import Task
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker



class TaskCreateform(forms.ModelForm):
    class Meta:
        model = Task
        #fields = '__all__'
        fields = ("title", "ZoomURL", "Start",  "Status","start_date")
        widgets = {
            #"Date": DatePicker,
            "start_date"  : DatePicker, 
            "Start": TimePicker,
           
        }

class TaskUpdateform(forms.ModelForm):
    class Meta:
        model = Task
        #fields = '__all__'
        fields = ("title", "ZoomURL", "Start", "deadline", "Status","start_date")
        widgets = {
            #"Date": DatePicker,
            "start_date"  : DatePicker, 
            "Start": TimePicker,
            "deadline": TimePicker,
        }

class EventForm(forms.Form):

    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)
    event_name = forms.CharField(required=True, max_length=32)
    
class CalendarForm(forms.Form):

    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)     
    # datetime_field = {
    #     "Start":forms.DateTimeField(
    #      widget=DateTimePicker(
    #             options={
    #                'useCurrent': True,
    #               'collapse': False,
    #             },
    #           attrs={
    #                'append': 'fa fa-calendar',
    #                'icon_toggle': True,
    #             }
    #         ),
    #     )
    # }
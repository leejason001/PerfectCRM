from django.forms import ModelForm
from django import forms

from crm import models

class Enrollment_Form( ModelForm ):
    class Meta:
        fields = "__all__"
        model = models.StudentEnrollment

class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            if field_name in cls.Meta.readonly_fields:
                filed_obj.widget.attrs.update({'disabled':'true'})
            filed_obj.widget.attrs.update({'class':'form-control'})

        return  ModelForm.__new__(cls)

    class Meta:
        fields = "__all__"
        exclude = ["consult_content", "status"]
        readonly_fields = ["contact_type","source", "consultant"]
        model  = models.CustomerInfo

    def clean(self):
        if self.errors:
            raise forms.ValidationError("Please fix errors first")
        if self.instance.id is not None:
            for field_name in self.Meta.readonly_fields:
                oldValue = getattr(self.instance, field_name)
                newValue = self.cleaned_data.get(field_name)
                if oldValue != newValue:
                    self.add_error(field_name, "Readonly field the value should be %s, not %s"%(oldValue, newValue))


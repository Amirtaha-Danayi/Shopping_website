from django import forms

class CouponApplyForm(forms):
    code = forms.CharField()
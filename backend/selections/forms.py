"""
选题表单
"""
from django import forms
from .models import Selection


class SelectionApplyForm(forms.Form):
    """选题申请表单"""
    reason = forms.CharField(
        label='申请理由',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '请简要说明您选择此题目的原因，包括您的相关背景、兴趣点等'
        }),
        required=True,
        min_length=10,
        max_length=500,
        error_messages={
            'required': '请填写申请理由',
            'min_length': '申请理由至少10个字符',
            'max_length': '申请理由不能超过500个字符',
        }
    )


class SelectionReviewForm(forms.Form):
    """选题审批表单"""
    comment = forms.CharField(
        label='审批意见',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': '请输入审批意见（可选）'
        }),
        required=False,
        max_length=500,
    )

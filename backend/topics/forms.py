"""
论文题目表单
"""
from django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    """论文题目表单"""
    
    class Meta:
        model = Topic
        fields = ['title', 'description', 'requirements', 'max_students']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入论文题目'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '请详细描述论文题目的研究内容、研究方向等'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请输入选题要求，如专业背景、技能要求等'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
        }
    
    def clean_max_students(self):
        max_students = self.cleaned_data.get('max_students')
        if max_students < 1:
            raise forms.ValidationError('最大可选人数至少为1')
        if max_students > 10:
            raise forms.ValidationError('最大可选人数不能超过10')
        return max_students

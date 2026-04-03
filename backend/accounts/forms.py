"""
账户相关表单
"""
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(
        label='用户名',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'autocomplete': 'current-password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise forms.ValidationError('该账户已被禁用')
            cleaned_data['user'] = user
        
        return cleaned_data


from .models import User
import re


class UserForm(forms.ModelForm):
    """用户表单（管理员用）"""
    password = forms.CharField(
        label='密码',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '留空则不修改密码'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'real_name', 'role', 'student_id', 'teacher_id', 'phone', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
            'real_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '真实姓名'}),
            'role': forms.Select(attrs={'class': 'form-control'}, choices=[(1, '学生'), (2, '教师')]),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '学号（学生填写）'}),
            'teacher_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '工号（教师填写）'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].help_text = '留空则不修改密码'
        else:
            self.fields['password'].required = True
            self.fields['password'].widget.attrs['placeholder'] = '请输入密码'
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not re.match(r'^1[3-9]\d{9}$', phone):
                raise forms.ValidationError('请输入正确的11位手机号')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise forms.ValidationError('请输入正确的邮箱格式')
        return email

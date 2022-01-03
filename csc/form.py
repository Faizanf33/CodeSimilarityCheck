from django import forms

from csc.models import User

class UploadFileForm(forms.ModelForm):
    
        # file = forms.FileField()
        # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        
    class Meta:
        model = User
        
        fields = ('profile_image',)
        
    def clean(self):
        """
        While User is updating his info, if he tries to change his
        password, Form is validated for fields Current Pasword and
        Confirm Password to ensure that User has not made a mistake
        while setting his new password.
        """
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        print("Clean is called")
        return cleaned_data

    # def save(self, request):
    #     """
    #     Updated values are fetched from Form after validation is applied on each
    #     field and if any new information is recieved then update User with it.
    #     """
    #     cleaned_data = super().clean()
    #     user = request.user
    #     if cleaned_data.get("full_name"):
    #         user.full_name = cleaned_data.get("full_name")
    #     if cleaned_data.get("cnic"):
    #         user.cnic = cleaned_data.get("cnic")
    #     if cleaned_data.get("credit_card"):
    #         user.credit_card_number = cleaned_data.get("credit_card")
    #     if len(request.FILES):
    #         user.profile_image = request.FILES["profile_image"]
    #     if cleaned_data.get("age"):
    #         user.age = cleaned_data.get("age")
    #     if cleaned_data.get("about_info"):
    #         user.about_info = cleaned_data.get("about_info")
    #     if cleaned_data.get("current_password"):
    #         user = self._update_current_user_password(user)
    #     user.save()
    
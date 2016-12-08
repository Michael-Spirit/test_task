from .forms import MyAuthenticationForm


def login_form(request):
    return {'login_form': MyAuthenticationForm()}

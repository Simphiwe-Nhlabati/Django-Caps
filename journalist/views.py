from django.shortcuts import render
from article.models import Article
from newsletter.models import Newsletter
from accounts.models import CustomUser


# Create your views here.
def journalist_dashboard(request):
    """
    View function for the journalist dashboard.
    This function renders the dashboard template for journalists.
    """
    journalist_option = CustomUser.objects.get(id=request.user.id)
    
    dash_list = {
        'articles': Article.objects.filter(journalist=journalist_option),
        'newsletters': Newsletter.objects.filter(journalist=journalist_option),
    }
    return render(request, 'journalist/journalist_dashboard.html', {'dash_list': dash_list})
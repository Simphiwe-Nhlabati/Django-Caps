from django.shortcuts import render
# from article.models import Article
# from newsletter.models import Newsletter
# from article.models import Publisher
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import CustomUser


# Create your views here.
def publisher_home(request):
    
    # if not request.user.is_authenticated or request.user.position != 'publisher':
    #     return redirect('home_view')
    
    # try:
    #     publisher = request.user.publisher
    # except Publisher.DoesNotExist:
    #     messages.error(request, 'You do not have permission to access this page.')
    #     return redirect('home_view') 

    if not request.user.is_authenticated or request.user.position != 'publisher':
        return redirect('home_view')

    editors = CustomUser.objects.filter(position='editor')
    journalists = CustomUser.objects.filter(position='journalist')

    news_list = {
        # 'publisher': publisher,
        'editors': editors,
        'journalists': journalists,
    }
    
    return render(request, 'publisher/publisher_dashboard.html', {'news_list': news_list})
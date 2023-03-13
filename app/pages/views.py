from django.views.generic import TemplateView

from app.models import Video
from app.utils import get_random


# Create your views here.

# Home page
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = Video.objects.all()

        context['random_videos'] = get_random(video, 6)
        return context


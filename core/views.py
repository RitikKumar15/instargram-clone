from django.shortcuts import redirect, render
from django.views.generic import View
from core.models import Post, Follow

# User Feed View Starts Here
class UserFeedView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      feed = []
      feed_post = Follow.objects.filter(user_id=request.user.id)
      for f in feed_post:
        feed.append([p for p in Post.objects.filter(user__id=f.followed_id)])
        flated_feed = []
        for sublist in feed:
          for elem in sublist:
            flated_feed.append(elem)
        remove_duplicates = set(flated_feed)
        final_feed = list(remove_duplicates)
        random.shuffle(final_feed)
      return render(request, 'core/tryfeed.html', {"feed": final_feed})
    else:
      return redirect('login')

from django.shortcuts import render_to_response
from django.template import RequestContext

from facegame.faceguessing.models import Player, UserStats
from facegame.faceguessing.views import get_user

from operator import itemgetter

def hall_of_fame(request):
    """ Displays top users by highest streaks """
    try:
        player = UserStats.objects.get(user=request.user)
    except:
        player = None
    hall_of_fame_list = Player.objects.all()
    hall_of_fame = []
    for item in hall_of_fame_list:
        if item.stats['highestStreak'] < 5:
            continue
        if not item.username:
            continue
        try:
            user = get_user(item.username)
        except Exception:
            continue
        hall_of_fame.append({"highestStreak": item.stats["highestStreak"], "wrongAnswers": item.stats["wrongAnswers"], 'user': user})
    hall_of_fame = sorted(hall_of_fame, key=itemgetter('highestStreak'), reverse=True)
    return render_to_response("hall_of_fame.html", {"player": player, 'hall_of_fame': hall_of_fame}, context_instance=RequestContext(request))


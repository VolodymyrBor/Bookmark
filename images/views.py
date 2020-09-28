import redis
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Image
from .forms import ImageCreateForm
from common.decorators import ajax_required
from actions.utils import create_action


r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


@login_required
def image_create(request: HttpRequest):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)

            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    context = {
        'section': 'images',
        'form': form,
    }

    return render(request, 'images/image/create.html', context)


def image_detail(request: HttpRequest, image_id: int, slug: str):
    image = get_object_or_404(Image, id=image_id, slug=slug)

    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', 1, image.id)

    context = {
        'section': 'images',
        'image': image,
        'total_views': total_views,
    }
    return render(request, 'images/image/detail.html', context)


@ajax_required
@login_required
@require_POST
def image_like(request: HttpRequest):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)

            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request: HttpRequest):
    images = Image.objects.all()
    paginator = Paginator(images, 16)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    context = {
        'section': 'images',
        'images': images,
    }

    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', context)

    return render(request, 'images/image/list.html', context)


@login_required
def image_ranking_view(request: HttpRequest):
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(image_id) for image_id in image_ranking]
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda image: image_ranking_ids.index(image.id))

    context = {
        'section': 'images',
        'most_viewed': most_viewed,
    }

    return render(request, 'images/image/ranking.html', context)

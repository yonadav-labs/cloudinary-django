from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from cloudinary.forms import cl_init_js_callbacks
import cloudinary.uploader
from .forms import FeedForm, FeedDirectForm
from .models import Loop
from django.utils import timezone


@login_required
def upload(request):
    direct_form = FeedDirectForm()
    context = dict(
        direct_form=direct_form,
    )
    # When using direct upload - the following call in necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

    return render(request, 'upload.html', context)


@login_required
def direct_upload_complete(request):
    # image = request.POST.image
    # post_values = request.POST.copy()
    form = FeedDirectForm(request.POST)
    public_id = request.POST.get('image')
    if public_id is not None:
        idx = public_id.find('/', 15)
        idx_e = public_id.find('.', 15)
        public_id = public_id[idx+1:idx_e]

    w_valid = form.is_valid()
    h_valid = form.errors == {'image': [u'No file selected!']}
    print request.POST.get('no_submit'), '@@@@@@@@@'
    if request.POST.get('no_submit') is not None:
        w_valid = h_valid = False

    if w_valid or h_valid:
        if w_valid:
            post = form.save(commit=False)
        else:
            post = Loop()
            post.created_at = timezone.now()
            post.text = request.POST['text']
            post.link = request.POST['link']
            post.image = ''
        post.user = request.user
        link = post.link
        idx = link.find('http://')
        idx = 0 if idx == -1 else idx + 7
        post.link = link[idx:]
        post.save()
        ret = dict(photo_id=form.instance.id)
        return render(request, 'upload_done.html')
    else:
        ret = dict(errors=form.errors)
        return HttpResponse(public_id, content_type='html/text')

    '''
    This is the json result what you want.
    You can configure it, and use it.
    '''
    # return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def delete_image(request, public_id):
    cloudinary.uploader.destroy(public_id)

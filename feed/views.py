import cloudinary.uploader
from cloudinary.forms import cl_init_js_callbacks
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import FeedDirectForm
from .models import Loop


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
    form = FeedDirectForm(request.POST)
    public_id = request.POST.get('image')

    # get the pure public_id of the image
    if public_id is not None:
        idx = public_id.find('/', 15)
        idx_e = public_id.find('.', 15)
        public_id = public_id[idx+1:idx_e]

    # in case required field is filled, save form
    w_valid = form.is_valid()
    h_valid = form.errors == {'image': [u'No file selected!']}

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
        # get rid of 'http://' from the link
        link = post.link
        idx = link.find('http://')
        idx = 0 if idx == -1 else idx + 7
        post.link = link[idx:]
        post.save()
        # redirect the success window
        return render(request, 'upload_done.html')
    else:
        return HttpResponse(public_id, content_type='html/text')


@csrf_exempt
def delete_image(request, public_id):
    '''
    delete image with public_id from cloudinary
    :param request:
    :param public_id: public_id of the iamge
    :return:
    '''
    cloudinary.uploader.destroy(public_id)

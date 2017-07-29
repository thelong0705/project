from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from rest_framework import authentication, permissions, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.routers import DefaultRouter
from .models import Document, Comment
from .forms import DocumentCreateForm
from rest_framework import viewsets, serializers


class AddNewDocumentView(LoginRequiredMixin, CreateView):
    form_class = DocumentCreateForm
    template_name = 'document/add_new_document.html'
    success_url = reverse_lazy('thankyou')

    def form_valid(self, form):
        form.instance.posted_user = self.request.user
        return super(AddNewDocumentView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'document/thank_you.html'


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document/document_detail.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating'] = self.object.userratedocument_set.all().aggregate(Avg('rating'))['rating__avg']
        return context


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = 'document/document_update.html'

    def render_to_response(self, context, **response_kwargs):
        if self.object.posted_user != self.request.user:
            return HttpResponseRedirect(reverse('no_permission'))
        return super().render_to_response(context, **response_kwargs)

    def get_success_url(self):
        return reverse('document_detail', kwargs={'id': self.get_object().id})


class DeleteDocumentView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'document/document_delete.html'
    success_url = reverse_lazy('index')

    def render_to_response(self, context, **response_kwargs):
        if self.object.posted_user != self.request.user:
            return HttpResponseRedirect(reverse('no_permission'))
        return super().render_to_response(context, **response_kwargs)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'document', 'content')


class NewPostCommentAPI(viewsets.GenericViewSet, ListCreateAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommentSerializer


router = DefaultRouter()
router.register('comment', NewPostCommentAPI, base_name='CommentAPI')
urlpatterns = router.urls


@login_required()
def like(request, pk):
    user = request.user
    document = get_object_or_404(Document, pk=pk)
    if user in document.liked_by.all():
        document.liked_by.remove(user)
        is_like = False
    else:
        document.liked_by.add(user)
        is_like = True
    data = {
        "is_like": is_like,
        "num_likes": document.liked_by.count()
    }
    return JsonResponse(data=data)

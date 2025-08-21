from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from .models import Occurrence, OccurrencePhoto
from .forms import OccurrenceForm, OccurrencePhotoForm

class OccurrenceListView(LoginRequiredMixin, ListView):
    model = Occurrence
    template_name = 'occurrences/list.html'
    paginate_by = 20

class OccurrenceDetailView(LoginRequiredMixin, DetailView):
    model = Occurrence
    template_name = 'occurrences/detail.html'

class OccurrenceCreateView(LoginRequiredMixin, CreateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = 'occurrences/form.html'
    success_url = reverse_lazy('occurrence_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.reported_by = self.request.user
        obj.save()
        return redirect('occurrence_detail', pk=obj.pk)

class OccurrenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = 'occurrences/form.html'

    def get_success_url(self):
        return reverse_lazy('occurrence_detail', kwargs={'pk': self.object.pk})

class OccurrencePhotoCreateView(LoginRequiredMixin, CreateView):
    model = OccurrencePhoto
    form_class = OccurrencePhotoForm
    template_name = 'occurrences/photo_form.html'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('occurrence_detail', kwargs={'pk': self.object.occurrence.pk})

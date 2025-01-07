from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import TechExample, WritingExample

# Homepage View
def home(request):
    tech_examples = TechExample.objects.all()
    writing_examples = WritingExample.objects.all()
    return render(request, 'portfolio/home.html', {
        'tech_examples': tech_examples,
        'writing_examples': writing_examples
    })

# Detail View for Tech Example
def tech_detail(request, pk):
    tech = get_object_or_404(TechExample, pk=pk)
    return render(request, 'portfolio/tech_detail.html', {'tech': tech})

# Detail View for Writing Example
def writing_detail(request, pk):
    writing = get_object_or_404(WritingExample, pk=pk)
    return render(request, 'portfolio/writing_detail.html', {'writing': writing})

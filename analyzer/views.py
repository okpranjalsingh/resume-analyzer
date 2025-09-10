from django.shortcuts import render
from .forms import ResumeForm
from .models import Resume
from .utils import extract_text_from_docx, extract_text_from_pdf

def home(request):
    extracted_text = None

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save()
            file_path = resume.file.path

            if file_path.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                extracted_text = extract_text_from_docx(file_path)
            else:
                extracted_text = "Unsupported file format."

            print(extracted_text)  # For debugging

        else:
            extracted_text = "Form is invalid. Please fill all fields correctly."

    else:
        form = ResumeForm()

    # Always return a response
    return render(request, 'analyzer/home.html', {'form': form, 'extracted_text': extracted_text})


def result(request):
    resumes = Resume.objects.all()
    return render(request, 'analyzer/results.html', {'resumes': resumes})

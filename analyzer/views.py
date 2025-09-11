from django.shortcuts import render
from .forms import ResumeForm
from .models import Resume
from .utils import extract_text_from_docx, extract_text_from_pdf
from django.http import HttpResponse
import re
import json
import csv


def home(request):
    return render(request, 'analyzer/home.html')

'''predefined keywords'''
SKILLS = ['Python', 'Django', 'DRF', 'FastAPI', 'SQL', 'MySQL', 'PostgreSQL',
          'HTML', 'CSS', 'JavaScript', 'Docker', 'Git', 'AWS', 'Postman']

EDUCATION_KEYWORDS = ['MCA', 'BCA', 'B.Tech', 'M.Tech', 'University', 'College']
EXPERIENCE_KEYWORDS = ['Intern', 'Developer', 'Backend', 'Engineer', 'Project', 'Trainee']

'''home page '''
def home(request):
    extracted_text = None
    resume_data = {}
    highlighted_text = None

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save()
            file_path = resume.file.path

            '''file text extraction'''
            if file_path.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                extracted_text = extract_text_from_docx(file_path)
            else:
                extracted_text = "Unsupported file format."

            ''' Extract mail + regex implement'''
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, extracted_text)
            email = emails[0] if emails else None
            
            ''' Extract Phone & regex implement'''
            phone_pattern = r'(\+?\d{1,3}[\s-]?)?\d{10}'
            phones = re.findall(phone_pattern, extracted_text)
            phone = phones[0] if phones else None

            '''extraction of the data to highlight'''
            found_skills = [skill for skill in SKILLS if skill.lower() in extracted_text.lower()]

            education_lines = [line.strip() for line in extracted_text.split('\n')
                               if any(keyword.lower() in line.lower() for keyword in EDUCATION_KEYWORDS)]

            experience_lines = [line.strip() for line in extracted_text.split('\n')
                                if any(keyword.lower() in line.lower() for keyword in EXPERIENCE_KEYWORDS)]

            '''prepare dict'''
            resume_data = {
                'id': resume.id,
                'name': resume.name,
                'email': email,
                'phone': phone,
                'skills': found_skills,
                'education': education_lines,
                'experience': experience_lines,
                'uploaded_at': str(resume.uploaded_at),
                'file_url': resume.file.url
            }

            '''session storage for download'''
            request.session['resume_data'] = resume_data

            '''highlight section'''
            highlighted_text = extracted_text
            for skill in found_skills:
                highlighted_text = re.sub(rf'(?i){re.escape(skill)}',
                                          f'<span class="highlight-skill">{skill}</span>',
                                          highlighted_text)
            for edu in education_lines:
                highlighted_text = re.sub(rf'(?i){re.escape(edu)}',
                                          f'<span class="highlight-education">{edu}</span>',
                                          highlighted_text)
            for exp in experience_lines:
                highlighted_text = re.sub(rf'(?i){re.escape(exp)}',
                                          f'<span class="highlight-experience">{exp}</span>',
                                          highlighted_text)

        else:
            extracted_text = "Form is invalid. Please fill all fields correctly."

    else:
        form = ResumeForm()

    return render(request, 'analyzer/home.html', {
        'form': form,
        'extracted_text': extracted_text,
        'resume_data': resume_data,
        'highlighted_text': highlighted_text
    })


'''history page'''
def history(request):
    resumes = Resume.objects.order_by('-uploaded_at')
    return render(request, 'analyzer/history.html', {'resumes': resumes})


''' Download JSON '''
def download_json(request):
    resume_id = request.GET.get('resume_id')
    if resume_id:
        try:
            resume = Resume.objects.get(id=resume_id)
            data = {
                'id': resume.id,
                'name': resume.name,
                'email': resume.email,
                'phone': resume.phone,
                'file_url': resume.file.url,
                'uploaded_at': str(resume.uploaded_at)
            }
        except Resume.DoesNotExist:
            return HttpResponse("Resume not found.", status=404)
    else:
        data = request.session.get('resume_data')
        if not data:
            return HttpResponse("No data to download.", status=400)

    response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="resume.json"'
    return response


'''download CSV'''
def download_csv(request):
    resume_id = request.GET.get('resume_id')
    if resume_id:
        try:
            resume = Resume.objects.get(id=resume_id)
            data = {
                'id': resume.id,
                'name': resume.name,
                'email': resume.email,
                'phone': resume.phone,
                'file_url': resume.file.url,
                'uploaded_at': str(resume.uploaded_at)
            }
        except Resume.DoesNotExist:
            return HttpResponse("Resume not found.", status=404)
    else:
        data = request.session.get('resume_data')
        if not data:
            return HttpResponse("No data to download.", status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="resume.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'File URL', 'Uploaded At'])
    writer.writerow([data.get('id', ''),
                     data.get('name', ''),
                     data.get('email', ''),
                     data.get('phone', ''),
                     data.get('file_url', ''),
                     data.get('uploaded_at', '')])
    return response


'''Result Page'''
def result(request):
    resumes = Resume.objects.all()
    return render(request, 'analyzer/results.html', {'resumes': resumes})





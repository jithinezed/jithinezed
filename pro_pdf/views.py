from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status
# from .models import Category, Product
from django.http import JsonResponse
from django.conf import settings
from .models import Template,EditedForm


from django.template import Context
from django.template.loader import render_to_string,get_template
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from .serializer import TemplateGetSerializer,EditedFormSerializer
import pdfkit
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request,template_id):
    # categories = Category.objects.all()
    # return render(request,'index.html',{'categories':categories})
    """Generate pdf."""
    # Model data
    # people = Person.objects.all().order_by('last_name')
    # Rendered
    # html_string = render_to_string('pdf.html', {'people': "people"})
    # b= Template(html_content = html_string)
    # b.save()
    obj = Template.objects.get(id=template_id)
    
    html = HTML(string=obj.html_content, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    # b= Template(html_content = html_string)
    # b.save()
    


    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_template_list(request):
    if request.method == "GET":
        try:
            template = Template.objects.filter(tab_type='waste')
            serializer = TemplateGetSerializer(template,many=True)
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No template available'}, status=status.HTTP_400_BAD_REQUEST)    

    if request.method == "POST":
        try:
            serializer = TemplateSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({'Success': 'Template Added','app_data': 'Template Added '}, status.HTTP_201_CREATED)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template upload failed'}, status=status.HTTP_400_BAD_REQUEST)            

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pump_get_template_list(request):
    if request.method == "GET":
        try:
            template = Template.objects.all(tab_type='pump')
            serializer = TemplateGetSerializer(template,many=True)
            return Response(serializer.data)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'No template available'}, status=status.HTTP_400_BAD_REQUEST)    

    if request.method == "POST":
        try:
            serializer = TemplateSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({'Success': 'Template Added','app_data': 'Template Added '}, status.HTTP_201_CREATED)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Template upload failed'}, status=status.HTTP_400_BAD_REQUEST)            

                        


@api_view(['POST',"GET"])
@permission_classes([IsAuthenticated])
def download_edited_pdf(request,):
    if request.method =="POST":
        try:
            from django.core.files.base import ContentFile
            import base64
            data  = EditedForm.objects.get(id=7)

            # file_data = ContentFile(base64.b64decode(fileData))
            # object.file.save(file_name, file_data)
            from io import BytesIO
            from weasyprint import HTML
            from weasyprint.pdf import PDFFile, pdf_format

            # html = HTML(string = data.html_content,base_url=request.build_absolute_uri())
            # print(html)
            # content = BytesIO(html.write_pdf())
            # print(content)
            # pdf_file = PDFFile(content)
            # print(pdf_file)
            # params = pdf_format('/OpenAction [0 /FitV null]')
            # print(params)
            # pdf_file.extend_dict(pdf_file.catalog, params)
            # le = pdf_file.finish()
            # pdf = pdf_file.fileobj.getvalue()
            # obj =EditedForm.objects.create(files=data.html_content)
            # open('/tmp/weasyprint.pdf', 'wb').write(pdf)


            # html_string = render_to_string(data.html_content, {'people': "people"})
            html = HTML(string=data.html_content, base_url=request.build_absolute_uri())
            
            result = html.write_pdf()
            obj =EditedForm.objects.create(files=result)
        
            

            # Creating http response
            
            return content

            # serializer =EditedFormSerializer(data= request.data)
            # if serializer.is_valid():
            #     try:
            #         form_obj = serializer.save()
            #         num =random.sample(range(1000000000,9999999999),1)
            #         random_number = str(num[0])
            #         url = 'media/pdf/_template.pdf'
            #         path = url[ : 10] + random_number + url[10 : ] 
            #         my_pdf = pdfkit.from_string(form_obj.html_content,path)
            #         return Response({'Success': 'File converted into pdf','app_data': path}, status.HTTP_201_CREATED)
            #     except Exception as E:
            #         return Response({'Error': str(E), 'app_data': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'Error': str(E), 'app_data': 'Generating pdf file failed '}, status=status.HTTP_400_BAD_REQUEST) 

    
    

        

    
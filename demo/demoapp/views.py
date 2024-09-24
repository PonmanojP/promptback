import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
import textwrap
from django.core.files.base import ContentFile
import base64
from .models import DashboardChart

GOOGLE_API_KEY='AIzaSyDtiq-CBPFG500PMG_UJtO08wf4EQnz9H4'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '', predicate=lambda _: True)

@csrf_exempt
def get_chart_data(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            prompt = request_data.get('message', '')

            instructions = f"""
                             - your task is to generate sql statement which is supported in mySQL for the given prompt for django environment this is very important.
                             - use simple functions rather than complex syntax that are not supported by MySQL env. Those functions should be understandable by Django mysql environment.
                             - the attributes of the database are gender, birth_date, emp_no, first_name, last_name, hire_date which is a primary key the table name is employees.
                             - the age format is 1953-09-02.
                             - give only the sql query. never give any explanation about the query never.
                             - query in such a way that it can be used to construct charts. the first column should be labels and the second column should be the values. hence query the columns accordingly.
                             - there should be only two columns. one should be labels(col1) and other should be values(col2). Query all the tuples as asked by the prompt.
                             - for each column, give alias like col1,col2 etc. This is veryy important..
                             - prompt = {prompt}.
                             - dont break the statements. give it in a single line.
                             - dont give the queries within any triple backticks and dont give any header like sql. please dont.
                             - if you find the user that he ask something else other than the database. just respond like "Sorry, I cannot respond to any other prompts that are not relevant to your database".
                            """
            
            response = model.generate_content(instructions)
            result = to_markdown(response.text).strip()
            

            query = f"{result}"
            print(query)
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]
            insights = get_insights(prompt,data)
            data.append({'col1':'others','insights':insights})
            print(data)
            
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error':'Sorry, I cannot respond to any other prompts that are not relevant to your database' }, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def save_chart_to_dashboard(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            description = data.get('description')
            chart_image_data = data.get('image')  # Base64 encoded image

            if not description or not chart_image_data:
                return JsonResponse({'error': 'Missing description or image data'}, status=400)

            # Decode the base64 image data
            format, imgstr = chart_image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'chart_{description[:10]}.{ext}')

            # Save to model
            dashboard_chart = DashboardChart(description=description, image=image_data)
            dashboard_chart.save()

            return JsonResponse({'success': 'Chart saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def get_insights(prompt, data):
    instructions = f'''
                    - You are given with the prompt and the result of the prompt.
                    - Your task is to analyse the prompt and the result array and provide the insights as human language(english).
                    - make your response within 50 words not exeeding it.
                    - prompt = {prompt}
                    - data = {data}
                    - Very Important : if you see any SQL error in the data just respond like this "Sorry, I cannot respond to any other prompts that are not relevant to your database".
                    - provide only relevant information not any explanations or exaggerations.
                    - never never describe the array and explain the user how you find out the information. just tell them your result. 
                    '''
    insights =model.generate_content(instructions)
    result = to_markdown(insights.text).strip()
    return result


def get_saved_charts(request):
    charts = DashboardChart.objects.all().order_by('-created_at')
    data = [{'description': chart.description, 'image': chart.image.url} for chart in charts][:6]
    return JsonResponse({'charts': data}, safe=False)


    

from django.shortcuts import render
from django.http import HttpResponse

import csv
import pandas as pd
from .models import Movie


# def index(request):
#     return render(request, 'main/index.html')

def result(request, u_id, demo):
    print("넘어온 : " + u_id + " " + demo)

    item = Movie.objects.all().values()
    df = pd.DataFrame(item)
    print(df.info())
    mdict = {
        "df": df.to_html()
    }
    return render(request, 'main/result.html', context=mdict)


# csv -> sqlite 데이터 넣는 2가지 방법
# sqlite 사용 python manage.py dbshell를 통해서 db에 넣기/ 2.django로 경로 만들어서 아래처럼 파일 읽어서 데이터 넣기
def csvToModel(request):

    path = "../renew_nefilx_titles.csv"
    file = open(path, 'rt', encoding="UTF8")
    reader = csv.reader(file)
    print("----", reader)    # 파일 읽어 왔는지 확인

    list = []
    for row in reader:
        print(row)
        list.append(Movie(show_id=row[0],
                               type =row[1],
                               title=row[2],
                               director=row[3],
                               cast=row[4],
                               country=row[5],
                               release_year=row[6],
                               rating=row[7],
                               duration=row[8],
                               listed_in=row[9],
                               description=row[10]))
    Movie.objects.bulk_create(list)

    # path = "renew_nefilx_titles.csv"
    #
    # with open(path, 'rt', encoding="UTF8", newline='') as csvfile:  # 4. newline =''
    #     data_reader = csv.DictReader(csvfile)
    #
    #     for row in data_reader:
    #         print(row)
    #         MovieModel.objects.create(
    #             show_id=row[0],
    #             type=row[1],
    #             title=row[2],
    #             director=row[3],
    #             cast=row[4],
    #             country=row[5],
    #             release_year=row[6],
    #             rating=row[7],
    #             duration=row[8],
    #             listed_in=row[9],
    #             description=row[10]
    #         )

    return HttpResponse('create model')

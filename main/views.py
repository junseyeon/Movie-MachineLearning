from django.shortcuts import render, redirect
from django.http import HttpResponse

import csv

from .models import MovieModel


# def index(request):
#     return render(request, 'index.html')


def csvToModel(request):

    #
    # path = "renew_nefilx_titles.csv"
    # file = open(path)
    # reader = csv.reader(file)
    # print("----", reader)    # 파일 읽어 왔는지 확인
    #
    # list = []
    # for row in reader:
    #     list.append(MovieModel(show_id=row[0],
    #                            type =row[1],
    #                            title=row[2],
    #                            director=row[3],
    #                            cast=row[4],
    #                            country=row[5],
    #                            release_year=row[6],
    #                            rating=row[7],
    #                            duration=row[8],
    #                            listed_in=row[9],
    #                            description=row[10]))

    return HttpResponse('create model')

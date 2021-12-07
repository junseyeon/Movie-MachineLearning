from django.shortcuts import render
from django.http import HttpResponse
from Login.models import UserInfo

import csv
import pandas as pd


from .models import Movie

# def index(request):
#     return render(request, 'main/index.html')


from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

import json


def result(request, nameid):
    print("result로 들어옴")

    item = Movie.objects.all().values()
    df = pd.DataFrame(item)

    df_combined = df['title'] + ' ' + df['description'] + ' ' + df['director'] + ' ' + df['cast'] + ' ' + df[
        'country'] + ' ' + df['rating'] + ' ' + df['listed_in']

    vectorizer = TfidfVectorizer(stop_words='english')
    df_vector = vectorizer.fit_transform(df_combined)

    # similarity = cosine_similarity(df_vector)
    similarity_des = linear_kernel(df_vector, df_vector)

    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    def get_recommendations(title, similarity_des=similarity_des):
        # Get the index of the movie that matches the title
        idx = indices[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(similarity_des[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return df.iloc[movie_indices]

    row = Movie.objects.get(show_id=int(nameid))           # 받아온 영화 id값으로 다시 title 찾기
    title = row.title

    df_Recommended = get_recommendations(title)

    # dataframe 스타일링 하기
    recommended = df_Recommended.to_html(classes='table table-striped')

    json_recommended = df_Recommended.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_recommended)
    context = {'recommended': data}

    return render(request, 'main/result.html', context=context)
    # return HttpResponse("완료")


def using(request, u_id):
    print("using 들어옴")
    row = UserInfo.objects.get(id=u_id)  # 받아온 id값으로 사용자 정보 찾기
    rating = row.rating
    listed_in = row.listed_in
    director = row.director
    cast = row.cast

    myFavorite = {
        'rating': rating,
        'listed_in': listed_in,
        'director': director,
        'cast': cast
    }

    item = Movie.objects.all().values()
    df = pd.DataFrame(item)

    def Recommand_Movie_with_Filter(filterList, favoriteList, df=df):
        cols = ['show_id', 'title', 'type', 'country', 'rating', 'listed_in', 'description']

        df_Filtered = df[[col for col in cols if (col not in filterList)]]

        favoriteDict = dict()
        for filteredCol in df_Filtered:
            if filteredCol in favoriteList.keys() and favoriteList[filteredCol] is not None:
                favoriteDict[filteredCol] = favoriteList[filteredCol]
            else:
                favoriteDict[filteredCol] = ''
        favoriteDict['title'] = '@'
        favoriteDict['show_id'] = int(df.tail(n=1)['show_id']) + 1

        df_Filtered = df_Filtered.append(favoriteDict, ignore_index=True)

        df_combined = df_Filtered.apply(lambda row: ' / '.join(row.values.astype(str)), axis=1)
        df_combined = df_combined.apply(lambda string: string[(string.find('/')) + 2:])
        vectorizer = TfidfVectorizer(stop_words='english')
        df_vector = vectorizer.fit_transform(df_combined)

        similarity = cosine_similarity(df_vector)
        similarity_des = linear_kernel(df_vector, df_vector)

        indices = pd.Series(df_Filtered.index, index=df_Filtered['title']).drop_duplicates()
        idx = indices['@']

        sim_scores = list(enumerate(similarity_des[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        df_recommand = df.copy()
        df_recommand = df_recommand.iloc[0:0]
        for title in list(df['title'].iloc[movie_indices]):
            df_recommand = df_recommand.append(df[df["title"] == title], ignore_index=True)
        df_recommand['similarRate'] = list(map(lambda tp: tp[1], sim_scores))

        return df_recommand

    pd.set_option('max_rows', 10, 'display.max_colwidth', 1000)
    recommendedMovies = Recommand_Movie_with_Filter([], myFavorite)

    json_recommended = recommendedMovies.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_recommended)
    context = {'recommended': data,
               'u_id' : u_id}

    return render(request, 'main/result.html', context=context)
    # return HttpResponse("응용 버전")


import seaborn as sns
import matplotlib.pyplot as plt


def manager(request):
    print("관리자------")
    # Plot된 그래프를 그림으로 저장 -> 저장된 그림을 웹에 띄움
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # BASE_DIR = os.path.abspath(__file__)
    path = './main/static/plot_png/'
    i = 1

    def count_plot(df, col):      # type / Movie or TV Show 비율 그래프
        sns.set_style("darkgrid")
        plt.figure(figsize=(12, 7))
        sns.countplot(x=col,
                      data=df,
                      order=df[col].value_counts().to_frame().index)
        plt.ylabel(f"Count of type {col}")
        plt.xlabel("Type")
        plt.title(f"Number of {col}", fontweight='bold', fontsize=15)

        plt.savefig(path + 'count_plot'+ str(i) +'.png', dpi=300)


    def country_plot():
        sns.set_style('darkgrid')
        plt.figure(figsize=(12, 10))
        sns.countplot(y=df['country'],
                      data=df,
                      order=df['country'].value_counts().index[0:10],
                      palette="Set1")
        plt.xlabel("Numberf of movie")
        plt.title("Number of movie each country", fontweight='bold', fontsize=15)
        plt.savefig(path + 'country_plot.png', dpi=300)

    def dist_plot(df, col):
        plt.figure(figsize=(12, 8))
        sns.distplot(df[col], color = "b")
        plt.title(f"Distribution of  {col} ", fontweight='bold', fontsize = 15)
        plt.savefig(path + 'dist_plot.png', dpi=150)

    item = Movie.objects.all().values()
    df = pd.DataFrame(item)
    count_plot(df, "type")
    i = i+1
    count_plot(df, "rating")
    country_plot()
    dist_plot(df, "release_year")

    return render(request, 'main/manager.html')


# csv -> sqlite 데이터 넣는 2가지 방법
# sqlite 사용 python manage.py dbshell를 통해서 db에 넣기/ 2.django로 경로 만들어서 아래처럼 파일 읽어서 데이터 넣기
def csvToModel(request):
    path = "../renew_nefilx_titles.csv"
    file = open(path, 'rt', encoding="UTF8")
    reader = csv.reader(file)
    print("----", reader)  # 파일 읽어 왔는지 확인

    list = []
    for row in reader:
        print(row)
        list.append(Movie(show_id=row[0],
                          type=row[1],
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

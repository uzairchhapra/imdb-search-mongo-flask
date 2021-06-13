from typing import List


from re import compile, IGNORECASE
from enum import Enum

def getOperatorQuery(values:list):
    if(values[0]=='>'):
        return {'$gt':float(values[1])}
    elif(values[0]=='>='):
        return {'$gte':float(values[1])}
    elif(values[0]=='<'):
        return {'$lt':float(values[1])}
    elif(values[0]=='<='):
        return {'$lte':float(values[1])}
    elif(values[0]=='='):
        return {'$eq':float(values[1])}
    elif(values[0]=='!='):
        return {'$ne':float(values[1])}


def customSearch(name:str, director:str, genre:list, _99popularity:list, imdb_score:list):
    query={}
    if name:
        query["name"]=compile(f'.*{name}.*', IGNORECASE)
    if director:
        query["director"]=compile(f'.*{director}.*', IGNORECASE)
    if genre:
        innerQuery = {}
        innerQuery['$all']=genre
        query['genre']=innerQuery
    if len(_99popularity)==2 and _99popularity[1]:
        innerQuery = getOperatorQuery(_99popularity)
        query['99popularity']=innerQuery
    if len(imdb_score)==2 and imdb_score[1]:
        innerQuery = getOperatorQuery(imdb_score)
        query['imdb_score']=innerQuery
    return query
        

# Docker-InsertSimilarityMatrix

This repositary contains the format for creating container which is deployed using docker

It is the module of recommendation system which reads data from mongodb and generate cosine similarity matrix and 
insert it in the mongodb which is used by 2nd module in repositary ( Docker-deployment-RecommenderSystem) to generate top n
recommendations.

Below is

Docker Hub image  :- https://hub.docker.com/r/ankitkislaya1995/insertrecsys_flask

API:- http://localhost:5000/insertmatrix

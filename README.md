# Project Description

## WikiRacer

## Description

We want to implement a WikiRacing game.  The game is as follows:
1. Users join a game, and are given a start point and end point.  They are presented with an interface that looks like [this](https://luke.deentaylor.com/wikipedia/).
2. Users must find a path through the graph from the start article to the end article.  Every time they expand an article, they are presented with a graph showing more articles.  The database tracks clicks.
3. When everyone finds a path, the game ends.  The people who expanded the fewest links win.
The database should track all of this, and be used to present visualizations and leaderboards.

## Usefulness

We believe that this game represents an interactive way to explore Wikipedia, one of the best sources of information about a variety of topics, and find out about more topics and articles that they may not have known about before. Furthermore, our recommendation features would help them find more relevant articles and information for them to explore once they are done playing the game.

## Realness

Out data will be parsed from Wikipedia. These data are publically available online. We will use a web crawler to crawl through wikipedia and create associations between links.

## Functionality
Basic functions:

- Get real data by crawling Wikipedia. Crawling Wikipedia for the article name and intro to set up the visualization part of the game.
- Players will be create an account to store their scores and accounts.
- Our player will be given a starting article and an ending article and will try to find the minimum path between.
- We’ll have a visualization for handling the user playing the game, allowing them to click on links in a user-friendly way.
- After the game, the user can get a score and store that onto a scoreboard. 

### Advanced Functions
- Visualization - After a user plays each round of the game, we want to generate 3 visualizations of the subset of the graph of articles that was relevant to the round that was played. One visualization would display the most optimal (shortest) path between the starting and ending articles. Another visualization would display the most commonly traveled path based on other users that have played the same round. Another visualization would display the overall user’s path and what other possible options they had. In this way, they can compare their performance with the most optimal solution and other people’s solutions, to understand how they can improve from round to round.
Post filter

- Web Crawler and Mapping - Another advanced feature would be a recommendation engine, which ties in directly with how we’ll be creating our web crawler. We’ll need to create a graph to represent the Wikipedia articles and how they are related through links. Using this graph, we would allow a user to type in an article, and we could generate a list of recommended articles. Our recommendations could also be based on other metrics such as categorizations from an NLP API through Watson. In addition, we would use this graph to verify that the randomly generated start and end Articles are within a certain difficulty based on the minimum number of links to go from one to another. This way, we could generate easy, medium, and hard games based on what the user requests, and also avoid trivial games such as the start and end Article being directly linked.

twitter-trends
==================
Using Twitter's Streaming API, to compute trends.

Currently at a very early stage.

Authentication to Twitter's API is handled by Leah Culver's oauth module. Can
be found at: ``http://oauth.googlecode.com/svn/code/python/oauth/oauth.py``

Architecture
------------

*   Main Thread: Initiates worker threads

    * Thread ``Listener``: Connects to the streaming API, reads the stream, 
      splits tweets into tokens, and updates the frequency table.

    * Thread ``Statistician``: Reads the frequency table and computer the trends.


*   Classes:
    
    * ``trends.api.stream.Stream``: Handles authentication to Twitter API. 
            
        * ``handler``: File-like object that listens to Twitter API.
        * ``connect()``: Opens the connection of the ``handler`` to the
          API.
        * ``get_tweet()``: Transforms a received JSON dictionary to a Tweet
          instance.
        *  ``close()``: Closes the connection of the ``handler`` to the API

    * ``trends.api.stream.Tweet``: Instances of this class represent tweet
      information.

        * ``text``: Tweet text 

        * ``get_tokens()``: Analyzes the ``text`` and returns its tokens.

    * ``trends.analysis.listener.Listener``: Facilitates the Stream class,
      to retrieve data from the Twitter API.

        * ``stream``: A ``Stream`` instance

    * ``trends.analysis.statistician.Stats``: Wrapper class around the data
      structure that will store token along with their statistics.

        * ``_scores``: Dictionary that stores pairs of `token`:`<TokenStats
          object>`

        * ``add(token)``: If no entry exists in dictionary ``_scores``
          for key `token`, an entry is created. Else, it's updated.

        * ``get_stats()``: Initiates the computation of stats for the tokens in
          ``_scores``.

    * ``trends.analysis.statistician.TokenStats``: Instances of this class maintain the statistics
      that correspond to a single token.

        * ``observation``: Observations of the token, within this round

        * ``rounds_observed``: Amount of rounds that this token has been
          observed at least once

        * ``mean``: Floating mean.

        * ``sqr_mean``: Floating square mean

        * ``std``: Floating Standard deviation

        * ``score``: Floating average z-score

        * ``increase()``: Increases the amount of observations for the
          corresponding token, by 1.      

        * ``compute_scores()``: Computes the score and all the statistical
          parameters.

        * ``zero()``: Zeros parameters ``observation`` and ``score``

    * ``trends.analysis.statistician.Statistician``: Analyzes the ``Stats`` class and computes statistics.


Diagram
----------
::


                                --------------
               +---------------  Main Thread   --------------+
               |                ---------------              |
               |                                             |
               |                                             |
               |                                             |
       ----------------                             --------------------
        Listener Thread                             Statistician Thread
       ----------------                             --------------------
          Stream   <-----------------+                      Stats
                                     |                  
                                     |
                                     |
                                     |
                                 Twitter API
            



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

    * ``trends.analysis.listener.Collection``: Wrapper around the data
      structure that will store token appearances in tweets.

        * ``_tokens``: Dictionary that stores pairs of `token`:`no. of
          appearances`

    * ``trends.analysis.statisticia.Statistician``: Analyzes the ``Collection`` and computes statistics.


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
          Stream   <-----------------+                  Collection 
          Collection                 |                  
                                     |
                                     |
                                     |
                                 Twitter API
            




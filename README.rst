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



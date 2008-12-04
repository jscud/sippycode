You can see this code running here: 

https://sippycode.appspot.com/article_editor

This is a blog post editor, or article editor if you prefer, which finds key
words in your text as you are writing and displays web search results on
those key words next to the editor.

The fundamental idea, is to have an environment in which relevant data is
brought to you as you work. You don't even need to go info hunting, our
computers can find relevant information and bring it to you.

I created this in just a few hours for MashupCamp8, and there are a few ideas
I had for future improvments. I probably won't get around to it, so feel free
to take this code and use as a foundation.

Recommended improvements:
    * A WSIWYG editor to create rich HTML instead of just plain text. 
          (I looked at tinyMCE but ran out of time.)
    * Search on combinations of keywords instead of just individual items
          identified by Calais.
    * Search other information sources, like news results, images, videos.
    * Search on multiple search engines. (Google has an easy to use Ajax
          search API, but I wanted to try something that was totally new to
          me.)

To run this yourself, you'll need to sign up for Google App Engine, then
change the app ID in app.yaml, then upload. You will probably also need to 
sign up for the Calais and Yahoo Search BOSS APIs and replace my API keys
in the code (article.py) with your own API keys.

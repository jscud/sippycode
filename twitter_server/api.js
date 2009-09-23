/* Copyright (C) 2007-2008 Jeffrey William Scudder
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
// A global object to provide a namespace for all classes and functions.
var q12 = {};

/**
 * Find a DOM element in the  by id.
 *
 * @param {String} targetId The id of the element.
 * @return {DOM Element} The DOM element in the document with the id.
 */
q12.gid = function(targetId) {
  return document.getElementById(targetId);
};

/**
 * Creates a new DOM element with the desired tag.
 *
 * @param {String} tag The type of tag to be created.
 * @return {DOM Element} The new DOM element.
 */
q12.c = function(tag) {
  return document.createElement(tag);
};

/**
 * Creates a text element containing the specified text.
 *
 * @param {String} text The contents of the text node.
 * @param {DOM Element} The new text node.
 */
q12.t = function(text) {
  return document.createTextNode(text);
};

/**
 * Joins the list using the empty strings.
 *
 * @param {Array} list List The list to convert to a string.
 * @param {String} The contents of the array joined.
 */
q12.j = function(list) {
  return list.join('');
};

/**
 * Removes a DOM element from the document.
 *
 * @param domElement The element to delete.
 */
q12.d = function(domElement) {
  domElement.parentNode.removeChild(domElement);
}

// These need cross browser testing. (Beware IE's issue with innerHTML on a
// p tag).
/**
 * Escapes the string to safe text sets the contents of the Dom element.
 * This function uses q12's toHtml function to convert the text into a form
 * acceptable within HTML.
 *
 * @param {DOM Element} domElement The node whose contents should be set.
 * @param {String} textString The string which should be escaped to display
 *     as HTML.
 */
q12.setText = function(domElement, textString) {
  domElement.innerHTML = q12.toHtml(textString);
};

/**
 * Escapes the string to safe text sets the contents of the Dom element.
 * This function uses q12's toHtml function to convert the text into a form
 * acceptable within HTML.
 *
 * @param {DOM Element} domElement The node whose contents should be set.
 * @param {String} htmlString A string of HTML to set the contents.
 */
q12.setHtml = function(domElement, htmlString) {
  domElement.innerHTML = htmlString;
};

/**
 * Forms a URL string from the components.
 *
 * @param {String} base The beginning of the URL.
 * @param {Object} params A dictionary of URL parameters and their values. 
 *     These keys and values are escaped and appended to the base of the 
 *     URL.
 * @return {String} A string composed of the base URL and the object's
 *     key values pairs as URL parameters.
 */ 
q12.url = function(base, params) {
  parameters = [];
  for (key in params) {
    parameters.push(escape(key) + '=' + escape(params[key]));
  }
  return [base, parameters.join('&')].join('?');
};

/**
 * Makes an HTTP request and sets a callback to be called on state 4.
 *
 * @param {String} httpVerb The HTTP action to perform, typical values
 *     are 'GET', 'POST', 'HEAD', 'PUT', 'DELETE'. 
 * @param {String} data The data to be sent with the request. Optional,
 *     should not be used in a GET, HEAD, or DELETE.
 * @param {String} url The URL to which the request will be made.
 * @param {Object} headers Key value pairs to include in the request as
 *     HTTP headers.
 * @param {Function} handler The funciton to be executed when the server's
 *     response has been fully received.
 */
q12.httpRequest = function(httpVerb, data, url, headers, handler) {
  var http = null;
  if (window.XMLHttpRequest) {
    http = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    http = new ActiveXObject('Microsoft.XMLHTTP');
  }
  if (http) {
    http.open(httpVerb, url, true);
    http.onreadystatechange = function() {
      if (http.readyState == 4) {
        handler(http);
      }
    };
    var propery = null;
    for (property in headers) {
      http.setRequestHeader(property, headers[property]);
    }
    http.send(data);
  } else {
    throw new Error('Unable to create the HTTP request object.');
  }
};

/**
 * Makes a GET request and calls the callback function.
 *
 * @param {String} url The target URL.
 * @param {Object} headers Key value pairs which are sent as HTTP 
 *     headers as part of the get request.
 * @param {Function} handler The function to be called when the server's
 *     response is ready.
 */
q12.get = function(url, headers, handler) {
  q12.httpRequest('GET', null, url, headers, handler);
};

q12.post = function(data, url, headers, handler) {
  q12.httpRequest('POST', data, url, headers, handler);
};

q12.put = function(data, url, headers, handler) {
  q12.httpRequest('PUT', data, url, headers, handler);
};

q12.del = function(url, headers, handler) {
  q12.httpRequest('DELETE', null, url, headers, handler);
};

q12.setCookie = function(name, value, days, path) {
  var expires = ''
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days*24*60*60*1000));
    expires = '; expires=' + date.toGMTString();
  }
  document.cookie = [name, '=', value, expires, '; path=', path].join(''); 
}

q12.getCookie = function(name) {
  var nameEQ = name + '=';
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) == 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

// Base 64 conversion code was written by Tyler Akins and has been placed 
// in the public domain.  It would be nice if you left this header intact.
// Base64 code from Tyler Akins -- http://rumkin.com
q12.b64KeyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw' + 
    'xyz0123456789+/=';

/**
 * Encodes the data in base64 encoding.
 *
 * @param {String} input The original data to be base 64 encoded.
 * @return {String} The input string in base64 encoding.
 */
q12.to64 = function(input) {
  var output = "";
  var chr1, chr2, chr3;
  var enc1, enc2, enc3, enc4;
  var i = 0;

  do {
    chr1 = input.charCodeAt(i++);
    chr2 = input.charCodeAt(i++);
    chr3 = input.charCodeAt(i++);

    enc1 = chr1 >> 2;
    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
    enc4 = chr3 & 63;

    if (isNaN(chr2)) {
      enc3 = enc4 = 64;
    } else if (isNaN(chr3)) {
      enc4 = 64;
    }

    output = [output, q12.b64KeyStr.charAt(enc1), 
              q12.b64KeyStr.charAt(enc2), 
              q12.b64KeyStr.charAt(enc3), 
              q12.b64KeyStr.charAt(enc4)].join('');
  } while (i < input.length);
   
  return output;
};

/**
 * Decodes the data from base 64 encoding.
 * 
 * @param {String} input A base64 encoded stirng to be decoded.
 * @return {String} The data decoded from base64 encoding.
 */
q12.from64 = function(input) {
  var output = "";
  var chr1, chr2, chr3;
  var enc1, enc2, enc3, enc4;
  var i = 0;

  // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
  input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

  do {
    enc1 = q12.b64KeyStr.indexOf(input.charAt(i++));
    enc2 = q12.b64KeyStr.indexOf(input.charAt(i++));
    enc3 = q12.b64KeyStr.indexOf(input.charAt(i++));
    enc4 = q12.b64KeyStr.indexOf(input.charAt(i++));

    chr1 = (enc1 << 2) | (enc2 >> 4);
    chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
    chr3 = ((enc3 & 3) << 6) | enc4;

    output = output + String.fromCharCode(chr1);

    if (enc3 != 64) {
      output = output + String.fromCharCode(chr2);
    }
    if (enc4 != 64) {
      output = output + String.fromCharCode(chr3);
    }
  } while (i < input.length);

  return output;
};

/**
 * Converts a string to into an equivalend form when displayed as HTML.
 * Performs HTML escaping on special characters in HTML and preserves 
 * spaces. The following characters are converted: &amp;, '  ',
 * &lt;, &gt;, &quot, and 
 * newline (converted to a line break).
 *
 * @param {String} input The original string to be escaped.
 * @return {String} An HTML version of the string.
 */
q12.toHtml = function(input) {
  // Replaces the following strings with their HTML code equivalents:
  // '&', '  ', '<', '>', '"', '\n'
  return input.replace(/&/g, '&amp;').replace(/  /g, '  '
      ).replace(/</g, '&lt;').replace(/>/g, '&gt;'
          ).replace(/"/g, '&quot;').replace(/\n/g, '<br/>');
};

/**
 * Reverses the HTML escaping from toHtml. 
 *
 * @param {String} input The HTML escaped string to be unescaped back to
 *     the original text.
 * @return {String} The original string with HTML escaping reversed.
 */
q12.fromHtml = function(input) {
  // Reverses the escape characters produced by toHtml.
  return input.replace(/<br\/>/g, '\n').replace(/&quot;/g, '"'
      ).replace(/&gt;/g, '>').replace(/&lt;/g, '<'
          ).replace(/  /g, '  ').replace(/&amp;/g, '&');
};

q12.toUrl = function(input) {
  return escape(input);
};

q12.fromUrl = function(input) {
  return unescape(input);
};

/* Entry point for our application. */
function start() {
  q12.setHtml(
      q12.gid('container'),
      '<input id="tweet" size="140"></input>'
      + '<button value="Tweet" onclick="tweet()">Tweet</button>'
      + '<div id="last-tweet"></div>'
      + '<button value="Newer" onclick="fetchNewer()">Newer</button>'
      + '<div id="feed"></div>'
      + '<button value="Older" onclick="fetchOlder()">Older</button>'
      );
}

function tweetResponseHandler(http) {
  var response = JSON.parse(http.responseText);
  q12.setText(q12.gid('last-tweet'), 'Your last tweet: ' + response.text);
}

function tweet() {
  q12.post(q12.gid('tweet').value, '/api', {'action': 'tweet'}, tweetResponseHandler);
}

function fetch() {
  q12.post('', '/api', {'action': 'read'}, readResponseHandler);
}

function fetchNewer() {
  if (newestUpdate == null) {
    fetch();
  } else {
    q12.post('', '/api', {'action': 'read', 'after': newestUpdate}, readResponseHandler);
  }
}

function fetchOlder() {
  if (oldestUpdate == null) {
    fetch();
  } else {
    q12.post('', '/api', {'action': 'read', 'before': oldestUpdate}, readResponseHandler);
  }
}

var oldestUpdate = null;
var newestUpdate = null;

function readResponseHandler(http) {
  var updates = JSON.parse(http.responseText);
  if (updates.length == 0) {
    return;
  }
  var profileImg = null;
  var updateContainer = null;
  var username = null;
  var prepend = false;
  // Set the oldest and newest if applicable.
  if (oldestUpdate == null || oldestUpdate >  updates[updates.length-1].id) {
    oldestUpdate = updates[updates.length-1].id;
  }
  if (newestUpdate == null || newestUpdate < updates[0].id) {
    newestUpdate = updates[0].id;
    prepend = true;
  }

  if (prepend) {
    for (var i = updates.length-1; i >= 0; i--) {
      // Check to see if the message already is on the page.
      if (q12.gid('t' + updates[i].id) == null) {
        // If the message is not present, render it.
        var feedNode = q12.gid('feed');
        feedNode.insertBefore(buildUpdateNode(updates[i]), feedNode.firstChild);
      }
    }
  } else { 
    // Render the messages.
    for (var i = 0; i < updates.length; i++) {
      // Check to see if the message already is on the page.
      if (q12.gid('t' + updates[i].id) == null) {
        // If the message is not present, render it.
        q12.gid('feed').appendChild(buildUpdateNode(updates[i]));
      }
    }
  }
  //q12.setText(q12.gid('feed'), http.responseText);
}

function buildUpdateNode(update) {
  var profileImg = q12.c('img');
  profileImg.src = update.user.profile_image_url;
  profileImg.setAttribute('class', 'user');
  var username = q12.c('a');
  username.href = 'http://twitter.com/' + update.user.screen_name;
  username.appendChild(q12.t(update.user.screen_name));
  var updateContainer = q12.c('div');
  updateContainer['id'] = 't' + update.id;
  updateContainer.appendChild(profileImg);
  updateContainer.appendChild(q12.t(' '));    
  updateContainer.appendChild(username);
  updateContainer.appendChild(q12.t(': '));    
  updateContainer.appendChild(q12.t(update.text));
  return updateContainer;
}

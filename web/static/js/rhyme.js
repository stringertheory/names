(function rhyme_o_matic () {
  var rhymes_div = $('#rhyme');
  var url = '/data/' + POEM_ID + '.json';
  $.getJSON(url, function (data) {

    var lookup = {}
    _.each(data.analyzed, function (sentence, s_i) {

      // make sentence
      var sentence_div = document.createElement('div');
      var attribute = document.createAttribute("class");
      attribute.value = "sentence";
      sentence_div.setAttributeNode(attribute);

      // go through each word
      _.each(sentence, function (word, w_i) {

	// make word
	var word_div = document.createElement('span');
	var attribute = document.createAttribute("class");
	attribute.value = "rhyme-word";
	word_div.setAttributeNode(attribute);
	var text = document.createTextNode(word.closest);
	word_div.appendChild(text);
	sentence_div.appendChild(word_div);
	
	// lookup rhymes
	var key = s_i + ',' + w_i;
	var value = data.rhymes[key];

	// add to mapping for later
	lookup[key] = $(word_div);
	
	// if there are rhyming words
	if (value !== undefined) {

	  // add linked words for later
	  _.each(value, function (pair) {
	    if (data.rhymes[pair] === undefined) {
	      data.rhymes[pair] = [key];
	    } else {
	      data.rhymes[pair].push(key);
	    }
	  });
	}
      });
      rhymes_div.append(sentence_div);
    });

    _.each(data.analyzed, function (sentence, s_i) {
      _.each(sentence, function (word, w_i) {
	var key = s_i + ',' + w_i;
	var word = lookup[key];
	var rhyme_words = [];
	_.each(data.rhymes[key], function (key) {
	  rhyme_words.push(lookup[key]);
	});
	word.mouseenter(function () {
	  word.addClass('primary');
	  _.each(rhyme_words, function (word) {
	    word.addClass('secondary');
	  });
	});
	word.mouseleave(function () {
	  word.removeClass('primary');
	  _.each(rhyme_words, function (word) {
	    word.removeClass('secondary');
	  });
	});
      });
    });
    
  });
  
})();

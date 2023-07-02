/*!
 * Lunr languages, `Thai` language
 * https://github.com/MihaiValentin/lunr-languages
 *
 * Copyright 2017, Keerati Thiwanruk
 * http://www.mozilla.org/MPL/
 */
/*!
 * based on
 * Snowball JavaScript Library v0.3
 * http://code.google.com/p/urim/
 * http://snowball.tartarus.org/
 *
 * Copyright 2010, Oleg Mazko
 * http://www.mozilla.org/MPL/
 */

/**
 * export the module via AMD, CommonJS or as a browser global
 * Export code from https://github.com/umdjs/umd/blob/master/returnExports.js
 */
;
(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(factory)
  } else if (typeof exports === 'object') {
    /**
     * Node. Does not work with strict CommonJS, but
     * only CommonJS-like environments that support module.exports,
     * like Node.
     */
    module.exports = factory()
  } else {
    // Browser globals (root is window)
    factory()(root.lunr);
  }
}(this, function() {
  /**
   * Just return a value to define the module export.
   * This example returns an object, but the module
   * can return a function as the exported value.
   */
  return function(lunr) {
    /* throw error if lunr is not yet included */
    if ('undefined' === typeof lunr) {
      throw new Error('Lunr is not present. Please include / require Lunr before this script.');
    }

    /* throw error if lunr stemmer support is not yet included */
    if ('undefined' === typeof lunr.stemmerSupport) {
      throw new Error('Lunr stemmer support is not present. Please include / require Lunr stemmer support before this script.');
    }

    /*
    Thai tokenization is the same to Japanense, which does not take into account spaces.
    So, it uses the same logic to assign tokenization function due to different Lunr versions.
    */
    var isLunr2 = lunr.version[0] == "2";

    /* register specific locale function */
    lunr.th = function() {
        this.pipeline.reset();
        this.pipeline.add(
            /*lunr.th.stopWordFilter,*/
            lunr.th.trimmer
        );

        if (isLunr2) { // for lunr version 2.0.0
            this.tokenizer = lunr.th.tokenizer;
        } else {
            if (lunr.tokenizer) { // for lunr version 0.6.0
                lunr.tokenizer = lunr.th.tokenizer;
            }
            if (this.tokenizerFn) { // for lunr version 0.7.0 -> 1.0.0
                this.tokenizerFn = lunr.th.tokenizer;
            }
        }
    };

    /* lunr trimmer function */
    lunr.th.wordCharacters = "[\u0e00-\u0e7f]";
    lunr.th.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.th.wordCharacters);
    lunr.Pipeline.registerFunction(lunr.th.trimmer, 'trimmer-th');

    var segmenter = lunr.wordcut;
    segmenter.init();
    lunr.th.tokenizer = function (obj) {
      //console.log(obj);
      if (!arguments.length || obj == null || obj == undefined) return []
      if (Array.isArray(obj)) return obj.map(function (t) { return isLunr2 ? new lunr.Token(t) : t })

      var str = obj.toString().replace(/^\s+/, '');
      return segmenter.cut(str).split('|');
    }
  };
}))

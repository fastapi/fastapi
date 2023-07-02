/*!
 * Lunr languages, `Vietnamese` language
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

    /* register specific locale function */
    lunr.vi = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.vi.stopWordFilter,
        lunr.vi.trimmer
      );
    };

    /* lunr trimmer function */
    lunr.vi.wordCharacters = "[" +
      "A-Za-z" +
      "\u0300\u0350" + // dấu huyền
      "\u0301\u0351" + // dấu sắc
      "\u0309" + // dấu hỏi
      "\u0323" + // dấu nặng
      "\u0303\u0343" + // dấu ngã
      "\u00C2\u00E2" + // Â
      "\u00CA\u00EA" + // Ê
      "\u00D4\u00F4" + // Ô
      "\u0102-\u0103" + // Ă
      "\u0110-\u0111" + // Đ
      "\u01A0-\u01A1" + // Ơ
      "\u01AF-\u01B0" + // Ư
      "]";
    lunr.vi.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.vi.wordCharacters);
    lunr.Pipeline.registerFunction(lunr.vi.trimmer, 'trimmer-vi');
    lunr.vi.stopWordFilter = lunr.generateStopWordFilter('là cái nhưng mà'.split(' '));
  };
}))
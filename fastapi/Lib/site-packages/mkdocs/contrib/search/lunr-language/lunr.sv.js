/*!
 * Lunr languages, `Swedish` language
 * https://github.com/MihaiValentin/lunr-languages
 *
 * Copyright 2014, Mihai Valentin
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
    lunr.sv = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.sv.trimmer,
        lunr.sv.stopWordFilter,
        lunr.sv.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.sv.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.sv.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.sv.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.sv.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.sv.trimmer, 'trimmer-sv');

    /* lunr stemmer function */
    lunr.sv.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function SwedishStemmer() {
          var a_0 = [new Among("a", -1, 1), new Among("arna", 0, 1),
              new Among("erna", 0, 1), new Among("heterna", 2, 1),
              new Among("orna", 0, 1), new Among("ad", -1, 1),
              new Among("e", -1, 1), new Among("ade", 6, 1),
              new Among("ande", 6, 1), new Among("arne", 6, 1),
              new Among("are", 6, 1), new Among("aste", 6, 1),
              new Among("en", -1, 1), new Among("anden", 12, 1),
              new Among("aren", 12, 1), new Among("heten", 12, 1),
              new Among("ern", -1, 1), new Among("ar", -1, 1),
              new Among("er", -1, 1), new Among("heter", 18, 1),
              new Among("or", -1, 1), new Among("s", -1, 2),
              new Among("as", 21, 1), new Among("arnas", 22, 1),
              new Among("ernas", 22, 1), new Among("ornas", 22, 1),
              new Among("es", 21, 1), new Among("ades", 26, 1),
              new Among("andes", 26, 1), new Among("ens", 21, 1),
              new Among("arens", 29, 1), new Among("hetens", 29, 1),
              new Among("erns", 21, 1), new Among("at", -1, 1),
              new Among("andet", -1, 1), new Among("het", -1, 1),
              new Among("ast", -1, 1)
            ],
            a_1 = [new Among("dd", -1, -1),
              new Among("gd", -1, -1), new Among("nn", -1, -1),
              new Among("dt", -1, -1), new Among("gt", -1, -1),
              new Among("kt", -1, -1), new Among("tt", -1, -1)
            ],
            a_2 = [
              new Among("ig", -1, 1), new Among("lig", 0, 1),
              new Among("els", -1, 1), new Among("fullt", -1, 3),
              new Among("l\u00F6st", -1, 2)
            ],
            g_v = [17, 65, 16, 1, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 32
            ],
            g_s_ending = [119, 127, 149],
            I_x, I_p1, sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function r_mark_regions() {
            var v_1, c = sbp.cursor + 3;
            I_p1 = sbp.limit;
            if (0 <= c || c <= sbp.limit) {
              I_x = c;
              while (true) {
                v_1 = sbp.cursor;
                if (sbp.in_grouping(g_v, 97, 246)) {
                  sbp.cursor = v_1;
                  break;
                }
                sbp.cursor = v_1;
                if (sbp.cursor >= sbp.limit)
                  return;
                sbp.cursor++;
              }
              while (!sbp.out_grouping(g_v, 97, 246)) {
                if (sbp.cursor >= sbp.limit)
                  return;
                sbp.cursor++;
              }
              I_p1 = sbp.cursor;
              if (I_p1 < I_x)
                I_p1 = I_x;
            }
          }

          function r_main_suffix() {
            var among_var, v_2 = sbp.limit_backward;
            if (sbp.cursor >= I_p1) {
              sbp.limit_backward = I_p1;
              sbp.cursor = sbp.limit;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_0, 37);
              sbp.limit_backward = v_2;
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    break;
                  case 2:
                    if (sbp.in_grouping_b(g_s_ending, 98, 121))
                      sbp.slice_del();
                    break;
                }
              }
            }
          }

          function r_consonant_pair() {
            var v_1 = sbp.limit_backward;
            if (sbp.cursor >= I_p1) {
              sbp.limit_backward = I_p1;
              sbp.cursor = sbp.limit;
              if (sbp.find_among_b(a_1, 7)) {
                sbp.cursor = sbp.limit;
                sbp.ket = sbp.cursor;
                if (sbp.cursor > sbp.limit_backward) {
                  sbp.bra = --sbp.cursor;
                  sbp.slice_del();
                }
              }
              sbp.limit_backward = v_1;
            }
          }

          function r_other_suffix() {
            var among_var, v_2;
            if (sbp.cursor >= I_p1) {
              v_2 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.cursor = sbp.limit;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_2, 5);
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    break;
                  case 2:
                    sbp.slice_from("l\u00F6s");
                    break;
                  case 3:
                    sbp.slice_from("full");
                    break;
                }
              }
              sbp.limit_backward = v_2;
            }
          }
          this.stem = function() {
            var v_1 = sbp.cursor;
            r_mark_regions();
            sbp.limit_backward = v_1;
            sbp.cursor = sbp.limit;
            r_main_suffix();
            sbp.cursor = sbp.limit;
            r_consonant_pair();
            sbp.cursor = sbp.limit;
            r_other_suffix();
            return true;
          }
        };

      /* and return a function that stems a word for the current locale */
      return function(token) {
        // for lunr version 2
        if (typeof token.update === "function") {
          return token.update(function(word) {
            st.setCurrent(word);
            st.stem();
            return st.getCurrent();
          })
        } else { // for lunr version <= 1
          st.setCurrent(token);
          st.stem();
          return st.getCurrent();
        }
      }
    })();

    lunr.Pipeline.registerFunction(lunr.sv.stemmer, 'stemmer-sv');

    lunr.sv.stopWordFilter = lunr.generateStopWordFilter('alla allt att av blev bli blir blivit de dem den denna deras dess dessa det detta dig din dina ditt du där då efter ej eller en er era ert ett från för ha hade han hans har henne hennes hon honom hur här i icke ingen inom inte jag ju kan kunde man med mellan men mig min mina mitt mot mycket ni nu när någon något några och om oss på samma sedan sig sin sina sitta själv skulle som så sådan sådana sådant till under upp ut utan vad var vara varför varit varje vars vart vem vi vid vilka vilkas vilken vilket vår våra vårt än är åt över'.split(' '));

    lunr.Pipeline.registerFunction(lunr.sv.stopWordFilter, 'stopWordFilter-sv');
  };
}))
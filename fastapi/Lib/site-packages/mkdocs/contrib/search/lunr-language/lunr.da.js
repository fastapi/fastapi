/*!
 * Lunr languages, `Danish` language
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
    lunr.da = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.da.trimmer,
        lunr.da.stopWordFilter,
        lunr.da.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.da.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.da.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.da.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.da.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.da.trimmer, 'trimmer-da');

    /* lunr stemmer function */
    lunr.da.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function DanishStemmer() {
          var a_0 = [new Among("hed", -1, 1), new Among("ethed", 0, 1),
              new Among("ered", -1, 1), new Among("e", -1, 1),
              new Among("erede", 3, 1), new Among("ende", 3, 1),
              new Among("erende", 5, 1), new Among("ene", 3, 1),
              new Among("erne", 3, 1), new Among("ere", 3, 1),
              new Among("en", -1, 1), new Among("heden", 10, 1),
              new Among("eren", 10, 1), new Among("er", -1, 1),
              new Among("heder", 13, 1), new Among("erer", 13, 1),
              new Among("s", -1, 2), new Among("heds", 16, 1),
              new Among("es", 16, 1), new Among("endes", 18, 1),
              new Among("erendes", 19, 1), new Among("enes", 18, 1),
              new Among("ernes", 18, 1), new Among("eres", 18, 1),
              new Among("ens", 16, 1), new Among("hedens", 24, 1),
              new Among("erens", 24, 1), new Among("ers", 16, 1),
              new Among("ets", 16, 1), new Among("erets", 28, 1),
              new Among("et", -1, 1), new Among("eret", 30, 1)
            ],
            a_1 = [
              new Among("gd", -1, -1), new Among("dt", -1, -1),
              new Among("gt", -1, -1), new Among("kt", -1, -1)
            ],
            a_2 = [
              new Among("ig", -1, 1), new Among("lig", 0, 1),
              new Among("elig", 1, 1), new Among("els", -1, 1),
              new Among("l\u00F8st", -1, 2)
            ],
            g_v = [17, 65, 16, 1, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 128
            ],
            g_s_ending = [239, 254, 42, 3,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16
            ],
            I_x, I_p1, S_ch, sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function r_mark_regions() {
            var v_1, c = sbp.cursor + 3;
            I_p1 = sbp.limit;
            if (0 <= c && c <= sbp.limit) {
              I_x = c;
              while (true) {
                v_1 = sbp.cursor;
                if (sbp.in_grouping(g_v, 97, 248)) {
                  sbp.cursor = v_1;
                  break;
                }
                sbp.cursor = v_1;
                if (v_1 >= sbp.limit)
                  return;
                sbp.cursor++;
              }
              while (!sbp.out_grouping(g_v, 97, 248)) {
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
            var among_var, v_1;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_0, 32);
              sbp.limit_backward = v_1;
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    break;
                  case 2:
                    if (sbp.in_grouping_b(g_s_ending, 97, 229))
                      sbp.slice_del();
                    break;
                }
              }
            }
          }

          function r_consonant_pair() {
            var v_1 = sbp.limit - sbp.cursor,
              v_2;
            if (sbp.cursor >= I_p1) {
              v_2 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              if (sbp.find_among_b(a_1, 4)) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_2;
                sbp.cursor = sbp.limit - v_1;
                if (sbp.cursor > sbp.limit_backward) {
                  sbp.cursor--;
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                }
              } else
                sbp.limit_backward = v_2;
            }
          }

          function r_other_suffix() {
            var among_var, v_1 = sbp.limit - sbp.cursor,
              v_2, v_3;
            sbp.ket = sbp.cursor;
            if (sbp.eq_s_b(2, "st")) {
              sbp.bra = sbp.cursor;
              if (sbp.eq_s_b(2, "ig"))
                sbp.slice_del();
            }
            sbp.cursor = sbp.limit - v_1;
            if (sbp.cursor >= I_p1) {
              v_2 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_2, 5);
              sbp.limit_backward = v_2;
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    v_3 = sbp.limit - sbp.cursor;
                    r_consonant_pair();
                    sbp.cursor = sbp.limit - v_3;
                    break;
                  case 2:
                    sbp.slice_from("l\u00F8s");
                    break;
                }
              }
            }
          }

          function r_undouble() {
            var v_1;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              if (sbp.out_grouping_b(g_v, 97, 248)) {
                sbp.bra = sbp.cursor;
                S_ch = sbp.slice_to(S_ch);
                sbp.limit_backward = v_1;
                if (sbp.eq_v_b(S_ch))
                  sbp.slice_del();
              } else
                sbp.limit_backward = v_1;
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
            sbp.cursor = sbp.limit;
            r_undouble();
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

    lunr.Pipeline.registerFunction(lunr.da.stemmer, 'stemmer-da');

    lunr.da.stopWordFilter = lunr.generateStopWordFilter('ad af alle alt anden at blev blive bliver da de dem den denne der deres det dette dig din disse dog du efter eller en end er et for fra ham han hans har havde have hende hendes her hos hun hvad hvis hvor i ikke ind jeg jer jo kunne man mange med meget men mig min mine mit mod ned noget nogle nu når og også om op os over på selv sig sin sine sit skal skulle som sådan thi til ud under var vi vil ville vor være været'.split(' '));

    lunr.Pipeline.registerFunction(lunr.da.stopWordFilter, 'stopWordFilter-da');
  };
}))
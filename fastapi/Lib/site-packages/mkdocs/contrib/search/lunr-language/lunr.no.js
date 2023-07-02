/*!
 * Lunr languages, `Norwegian` language
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
    lunr.no = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.no.trimmer,
        lunr.no.stopWordFilter,
        lunr.no.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.no.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.no.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.no.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.no.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.no.trimmer, 'trimmer-no');

    /* lunr stemmer function */
    lunr.no.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function NorwegianStemmer() {
          var a_0 = [new Among("a", -1, 1), new Among("e", -1, 1),
              new Among("ede", 1, 1), new Among("ande", 1, 1),
              new Among("ende", 1, 1), new Among("ane", 1, 1),
              new Among("ene", 1, 1), new Among("hetene", 6, 1),
              new Among("erte", 1, 3), new Among("en", -1, 1),
              new Among("heten", 9, 1), new Among("ar", -1, 1),
              new Among("er", -1, 1), new Among("heter", 12, 1),
              new Among("s", -1, 2), new Among("as", 14, 1),
              new Among("es", 14, 1), new Among("edes", 16, 1),
              new Among("endes", 16, 1), new Among("enes", 16, 1),
              new Among("hetenes", 19, 1), new Among("ens", 14, 1),
              new Among("hetens", 21, 1), new Among("ers", 14, 1),
              new Among("ets", 14, 1), new Among("et", -1, 1),
              new Among("het", 25, 1), new Among("ert", -1, 3),
              new Among("ast", -1, 1)
            ],
            a_1 = [new Among("dt", -1, -1),
              new Among("vt", -1, -1)
            ],
            a_2 = [new Among("leg", -1, 1),
              new Among("eleg", 0, 1), new Among("ig", -1, 1),
              new Among("eig", 2, 1), new Among("lig", 2, 1),
              new Among("elig", 4, 1), new Among("els", -1, 1),
              new Among("lov", -1, 1), new Among("elov", 7, 1),
              new Among("slov", 7, 1), new Among("hetslov", 9, 1)
            ],
            g_v = [17,
              65, 16, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 0, 128
            ],
            g_s_ending = [
              119, 125, 149, 1
            ],
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
                if (sbp.in_grouping(g_v, 97, 248)) {
                  sbp.cursor = v_1;
                  break;
                }
                if (v_1 >= sbp.limit)
                  return;
                sbp.cursor = v_1 + 1;
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
            var among_var, v_1, v_2;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_0, 29);
              sbp.limit_backward = v_1;
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    break;
                  case 2:
                    v_2 = sbp.limit - sbp.cursor;
                    if (sbp.in_grouping_b(g_s_ending, 98, 122))
                      sbp.slice_del();
                    else {
                      sbp.cursor = sbp.limit - v_2;
                      if (sbp.eq_s_b(1, "k") &&
                        sbp.out_grouping_b(g_v, 97, 248))
                        sbp.slice_del();
                    }
                    break;
                  case 3:
                    sbp.slice_from("er");
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
              if (sbp.find_among_b(a_1, 2)) {
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
            var among_var, v_1;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_2, 11);
              if (among_var) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_1;
                if (among_var == 1)
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

    lunr.Pipeline.registerFunction(lunr.no.stemmer, 'stemmer-no');

    lunr.no.stopWordFilter = lunr.generateStopWordFilter('alle at av bare begge ble blei bli blir blitt både båe da de deg dei deim deira deires dem den denne der dere deres det dette di din disse ditt du dykk dykkar då eg ein eit eitt eller elles en enn er et ett etter for fordi fra før ha hadde han hans har hennar henne hennes her hjå ho hoe honom hoss hossen hun hva hvem hver hvilke hvilken hvis hvor hvordan hvorfor i ikke ikkje ikkje ingen ingi inkje inn inni ja jeg kan kom korleis korso kun kunne kva kvar kvarhelst kven kvi kvifor man mange me med medan meg meget mellom men mi min mine mitt mot mykje ned no noe noen noka noko nokon nokor nokre nå når og også om opp oss over på samme seg selv si si sia sidan siden sin sine sitt sjøl skal skulle slik so som som somme somt så sånn til um upp ut uten var vart varte ved vere verte vi vil ville vore vors vort vår være være vært å'.split(' '));

    lunr.Pipeline.registerFunction(lunr.no.stopWordFilter, 'stopWordFilter-no');
  };
}))
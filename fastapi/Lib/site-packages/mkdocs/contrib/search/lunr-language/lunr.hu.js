/*!
 * Lunr languages, `Hungarian` language
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
    lunr.hu = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.hu.trimmer,
        lunr.hu.stopWordFilter,
        lunr.hu.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.hu.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.hu.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.hu.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.hu.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.hu.trimmer, 'trimmer-hu');

    /* lunr stemmer function */
    lunr.hu.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function HungarianStemmer() {
          var a_0 = [new Among("cs", -1, -1), new Among("dzs", -1, -1),
              new Among("gy", -1, -1), new Among("ly", -1, -1),
              new Among("ny", -1, -1), new Among("sz", -1, -1),
              new Among("ty", -1, -1), new Among("zs", -1, -1)
            ],
            a_1 = [
              new Among("\u00E1", -1, 1), new Among("\u00E9", -1, 2)
            ],
            a_2 = [
              new Among("bb", -1, -1), new Among("cc", -1, -1),
              new Among("dd", -1, -1), new Among("ff", -1, -1),
              new Among("gg", -1, -1), new Among("jj", -1, -1),
              new Among("kk", -1, -1), new Among("ll", -1, -1),
              new Among("mm", -1, -1), new Among("nn", -1, -1),
              new Among("pp", -1, -1), new Among("rr", -1, -1),
              new Among("ccs", -1, -1), new Among("ss", -1, -1),
              new Among("zzs", -1, -1), new Among("tt", -1, -1),
              new Among("vv", -1, -1), new Among("ggy", -1, -1),
              new Among("lly", -1, -1), new Among("nny", -1, -1),
              new Among("tty", -1, -1), new Among("ssz", -1, -1),
              new Among("zz", -1, -1)
            ],
            a_3 = [new Among("al", -1, 1),
              new Among("el", -1, 2)
            ],
            a_4 = [new Among("ba", -1, -1),
              new Among("ra", -1, -1), new Among("be", -1, -1),
              new Among("re", -1, -1), new Among("ig", -1, -1),
              new Among("nak", -1, -1), new Among("nek", -1, -1),
              new Among("val", -1, -1), new Among("vel", -1, -1),
              new Among("ul", -1, -1), new Among("n\u00E1l", -1, -1),
              new Among("n\u00E9l", -1, -1), new Among("b\u00F3l", -1, -1),
              new Among("r\u00F3l", -1, -1), new Among("t\u00F3l", -1, -1),
              new Among("b\u00F5l", -1, -1), new Among("r\u00F5l", -1, -1),
              new Among("t\u00F5l", -1, -1), new Among("\u00FCl", -1, -1),
              new Among("n", -1, -1), new Among("an", 19, -1),
              new Among("ban", 20, -1), new Among("en", 19, -1),
              new Among("ben", 22, -1), new Among("k\u00E9ppen", 22, -1),
              new Among("on", 19, -1), new Among("\u00F6n", 19, -1),
              new Among("k\u00E9pp", -1, -1), new Among("kor", -1, -1),
              new Among("t", -1, -1), new Among("at", 29, -1),
              new Among("et", 29, -1), new Among("k\u00E9nt", 29, -1),
              new Among("ank\u00E9nt", 32, -1), new Among("enk\u00E9nt", 32, -1),
              new Among("onk\u00E9nt", 32, -1), new Among("ot", 29, -1),
              new Among("\u00E9rt", 29, -1), new Among("\u00F6t", 29, -1),
              new Among("hez", -1, -1), new Among("hoz", -1, -1),
              new Among("h\u00F6z", -1, -1), new Among("v\u00E1", -1, -1),
              new Among("v\u00E9", -1, -1)
            ],
            a_5 = [new Among("\u00E1n", -1, 2),
              new Among("\u00E9n", -1, 1), new Among("\u00E1nk\u00E9nt", -1, 3)
            ],
            a_6 = [
              new Among("stul", -1, 2), new Among("astul", 0, 1),
              new Among("\u00E1stul", 0, 3), new Among("st\u00FCl", -1, 2),
              new Among("est\u00FCl", 3, 1), new Among("\u00E9st\u00FCl", 3, 4)
            ],
            a_7 = [
              new Among("\u00E1", -1, 1), new Among("\u00E9", -1, 2)
            ],
            a_8 = [
              new Among("k", -1, 7), new Among("ak", 0, 4),
              new Among("ek", 0, 6), new Among("ok", 0, 5),
              new Among("\u00E1k", 0, 1), new Among("\u00E9k", 0, 2),
              new Among("\u00F6k", 0, 3)
            ],
            a_9 = [new Among("\u00E9i", -1, 7),
              new Among("\u00E1\u00E9i", 0, 6), new Among("\u00E9\u00E9i", 0, 5),
              new Among("\u00E9", -1, 9), new Among("k\u00E9", 3, 4),
              new Among("ak\u00E9", 4, 1), new Among("ek\u00E9", 4, 1),
              new Among("ok\u00E9", 4, 1), new Among("\u00E1k\u00E9", 4, 3),
              new Among("\u00E9k\u00E9", 4, 2), new Among("\u00F6k\u00E9", 4, 1),
              new Among("\u00E9\u00E9", 3, 8)
            ],
            a_10 = [new Among("a", -1, 18),
              new Among("ja", 0, 17), new Among("d", -1, 16),
              new Among("ad", 2, 13), new Among("ed", 2, 13),
              new Among("od", 2, 13), new Among("\u00E1d", 2, 14),
              new Among("\u00E9d", 2, 15), new Among("\u00F6d", 2, 13),
              new Among("e", -1, 18), new Among("je", 9, 17),
              new Among("nk", -1, 4), new Among("unk", 11, 1),
              new Among("\u00E1nk", 11, 2), new Among("\u00E9nk", 11, 3),
              new Among("\u00FCnk", 11, 1), new Among("uk", -1, 8),
              new Among("juk", 16, 7), new Among("\u00E1juk", 17, 5),
              new Among("\u00FCk", -1, 8), new Among("j\u00FCk", 19, 7),
              new Among("\u00E9j\u00FCk", 20, 6), new Among("m", -1, 12),
              new Among("am", 22, 9), new Among("em", 22, 9),
              new Among("om", 22, 9), new Among("\u00E1m", 22, 10),
              new Among("\u00E9m", 22, 11), new Among("o", -1, 18),
              new Among("\u00E1", -1, 19), new Among("\u00E9", -1, 20)
            ],
            a_11 = [
              new Among("id", -1, 10), new Among("aid", 0, 9),
              new Among("jaid", 1, 6), new Among("eid", 0, 9),
              new Among("jeid", 3, 6), new Among("\u00E1id", 0, 7),
              new Among("\u00E9id", 0, 8), new Among("i", -1, 15),
              new Among("ai", 7, 14), new Among("jai", 8, 11),
              new Among("ei", 7, 14), new Among("jei", 10, 11),
              new Among("\u00E1i", 7, 12), new Among("\u00E9i", 7, 13),
              new Among("itek", -1, 24), new Among("eitek", 14, 21),
              new Among("jeitek", 15, 20), new Among("\u00E9itek", 14, 23),
              new Among("ik", -1, 29), new Among("aik", 18, 26),
              new Among("jaik", 19, 25), new Among("eik", 18, 26),
              new Among("jeik", 21, 25), new Among("\u00E1ik", 18, 27),
              new Among("\u00E9ik", 18, 28), new Among("ink", -1, 20),
              new Among("aink", 25, 17), new Among("jaink", 26, 16),
              new Among("eink", 25, 17), new Among("jeink", 28, 16),
              new Among("\u00E1ink", 25, 18), new Among("\u00E9ink", 25, 19),
              new Among("aitok", -1, 21), new Among("jaitok", 32, 20),
              new Among("\u00E1itok", -1, 22), new Among("im", -1, 5),
              new Among("aim", 35, 4), new Among("jaim", 36, 1),
              new Among("eim", 35, 4), new Among("jeim", 38, 1),
              new Among("\u00E1im", 35, 2), new Among("\u00E9im", 35, 3)
            ],
            g_v = [
              17, 65, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 17, 52, 14
            ],
            I_p1, sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function r_mark_regions() {
            var v_1 = sbp.cursor,
              v_2;
            I_p1 = sbp.limit;
            if (sbp.in_grouping(g_v, 97, 252)) {
              while (true) {
                v_2 = sbp.cursor;
                if (sbp.out_grouping(g_v, 97, 252)) {
                  sbp.cursor = v_2;
                  if (!sbp.find_among(a_0, 8)) {
                    sbp.cursor = v_2;
                    if (v_2 < sbp.limit)
                      sbp.cursor++;
                  }
                  I_p1 = sbp.cursor;
                  return;
                }
                sbp.cursor = v_2;
                if (v_2 >= sbp.limit) {
                  I_p1 = v_2;
                  return;
                }
                sbp.cursor++;
              }
            }
            sbp.cursor = v_1;
            if (sbp.out_grouping(g_v, 97, 252)) {
              while (!sbp.in_grouping(g_v, 97, 252)) {
                if (sbp.cursor >= sbp.limit)
                  return;
                sbp.cursor++;
              }
              I_p1 = sbp.cursor;
            }
          }

          function r_R1() {
            return I_p1 <= sbp.cursor;
          }

          function r_v_ending() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_1, 2);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                    sbp.slice_from("a");
                    break;
                  case 2:
                    sbp.slice_from("e");
                    break;
                }
              }
            }
          }

          function r_double() {
            var v_1 = sbp.limit - sbp.cursor;
            if (!sbp.find_among_b(a_2, 23))
              return false;
            sbp.cursor = sbp.limit - v_1;
            return true;
          }

          function r_undouble() {
            if (sbp.cursor > sbp.limit_backward) {
              sbp.cursor--;
              sbp.ket = sbp.cursor;
              var c = sbp.cursor - 1;
              if (sbp.limit_backward <= c && c <= sbp.limit) {
                sbp.cursor = c;
                sbp.bra = c;
                sbp.slice_del();
              }
            }
          }

          function r_instrum() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_3, 2);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                if (among_var == 1 || among_var == 2)
                  if (!r_double())
                    return;
                sbp.slice_del();
                r_undouble();
              }
            }
          }

          function r_case() {
            sbp.ket = sbp.cursor;
            if (sbp.find_among_b(a_4, 44)) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                sbp.slice_del();
                r_v_ending();
              }
            }
          }

          function r_case_special() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_5, 3);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                    sbp.slice_from("e");
                    break;
                  case 2:
                  case 3:
                    sbp.slice_from("a");
                    break;
                }
              }
            }
          }

          function r_case_other() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_6, 6);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                  case 2:
                    sbp.slice_del();
                    break;
                  case 3:
                    sbp.slice_from("a");
                    break;
                  case 4:
                    sbp.slice_from("e");
                    break;
                }
              }
            }
          }

          function r_factive() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_7, 2);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                if (among_var == 1 || among_var == 2)
                  if (!r_double())
                    return;
                sbp.slice_del();
                r_undouble()
              }
            }
          }

          function r_plural() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_8, 7);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                    sbp.slice_from("a");
                    break;
                  case 2:
                    sbp.slice_from("e");
                    break;
                  case 3:
                  case 4:
                  case 5:
                  case 6:
                  case 7:
                    sbp.slice_del();
                    break;
                }
              }
            }
          }

          function r_owned() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_9, 12);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                  case 4:
                  case 7:
                  case 9:
                    sbp.slice_del();
                    break;
                  case 2:
                  case 5:
                  case 8:
                    sbp.slice_from("e");
                    break;
                  case 3:
                  case 6:
                    sbp.slice_from("a");
                    break;
                }
              }
            }
          }

          function r_sing_owner() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_10, 31);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                  case 4:
                  case 7:
                  case 8:
                  case 9:
                  case 12:
                  case 13:
                  case 16:
                  case 17:
                  case 18:
                    sbp.slice_del();
                    break;
                  case 2:
                  case 5:
                  case 10:
                  case 14:
                  case 19:
                    sbp.slice_from("a");
                    break;
                  case 3:
                  case 6:
                  case 11:
                  case 15:
                  case 20:
                    sbp.slice_from("e");
                    break;
                }
              }
            }
          }

          function r_plur_owner() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_11, 42);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                  case 4:
                  case 5:
                  case 6:
                  case 9:
                  case 10:
                  case 11:
                  case 14:
                  case 15:
                  case 16:
                  case 17:
                  case 20:
                  case 21:
                  case 24:
                  case 25:
                  case 26:
                  case 29:
                    sbp.slice_del();
                    break;
                  case 2:
                  case 7:
                  case 12:
                  case 18:
                  case 22:
                  case 27:
                    sbp.slice_from("a");
                    break;
                  case 3:
                  case 8:
                  case 13:
                  case 19:
                  case 23:
                  case 28:
                    sbp.slice_from("e");
                    break;
                }
              }
            }
          }
          this.stem = function() {
            var v_1 = sbp.cursor;
            r_mark_regions();
            sbp.limit_backward = v_1;
            sbp.cursor = sbp.limit;
            r_instrum();
            sbp.cursor = sbp.limit;
            r_case();
            sbp.cursor = sbp.limit;
            r_case_special();
            sbp.cursor = sbp.limit;
            r_case_other();
            sbp.cursor = sbp.limit;
            r_factive();
            sbp.cursor = sbp.limit;
            r_owned();
            sbp.cursor = sbp.limit;
            r_sing_owner();
            sbp.cursor = sbp.limit;
            r_plur_owner();
            sbp.cursor = sbp.limit;
            r_plural();
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

    lunr.Pipeline.registerFunction(lunr.hu.stemmer, 'stemmer-hu');

    lunr.hu.stopWordFilter = lunr.generateStopWordFilter('a abban ahhoz ahogy ahol aki akik akkor alatt amely amelyek amelyekben amelyeket amelyet amelynek ami amikor amit amolyan amíg annak arra arról az azok azon azonban azt aztán azután azzal azért be belül benne bár cikk cikkek cikkeket csak de e ebben eddig egy egyes egyetlen egyik egyre egyéb egész ehhez ekkor el ellen elsõ elég elõ elõször elõtt emilyen ennek erre ez ezek ezen ezt ezzel ezért fel felé hanem hiszen hogy hogyan igen ill ill. illetve ilyen ilyenkor ismét ison itt jobban jó jól kell kellett keressünk keresztül ki kívül között közül legalább legyen lehet lehetett lenne lenni lesz lett maga magát majd majd meg mellett mely melyek mert mi mikor milyen minden mindenki mindent mindig mint mintha mit mivel miért most már más másik még míg nagy nagyobb nagyon ne nekem neki nem nincs néha néhány nélkül olyan ott pedig persze rá s saját sem semmi sok sokat sokkal szemben szerint szinte számára talán tehát teljes tovább továbbá több ugyanis utolsó után utána vagy vagyis vagyok valaki valami valamint való van vannak vele vissza viszont volna volt voltak voltam voltunk által általában át én éppen és így õ õk õket össze úgy új újabb újra'.split(' '));

    lunr.Pipeline.registerFunction(lunr.hu.stopWordFilter, 'stopWordFilter-hu');
  };
}))
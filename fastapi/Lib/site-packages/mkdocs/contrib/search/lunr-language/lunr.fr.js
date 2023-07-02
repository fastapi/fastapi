/*!
 * Lunr languages, `French` language
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
    lunr.fr = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.fr.trimmer,
        lunr.fr.stopWordFilter,
        lunr.fr.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.fr.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.fr.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.fr.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.fr.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.fr.trimmer, 'trimmer-fr');

    /* lunr stemmer function */
    lunr.fr.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function FrenchStemmer() {
          var a_0 = [new Among("col", -1, -1), new Among("par", -1, -1),
              new Among("tap", -1, -1)
            ],
            a_1 = [new Among("", -1, 4),
              new Among("I", 0, 1), new Among("U", 0, 2), new Among("Y", 0, 3)
            ],
            a_2 = [
              new Among("iqU", -1, 3), new Among("abl", -1, 3),
              new Among("I\u00E8r", -1, 4), new Among("i\u00E8r", -1, 4),
              new Among("eus", -1, 2), new Among("iv", -1, 1)
            ],
            a_3 = [
              new Among("ic", -1, 2), new Among("abil", -1, 1),
              new Among("iv", -1, 3)
            ],
            a_4 = [new Among("iqUe", -1, 1),
              new Among("atrice", -1, 2), new Among("ance", -1, 1),
              new Among("ence", -1, 5), new Among("logie", -1, 3),
              new Among("able", -1, 1), new Among("isme", -1, 1),
              new Among("euse", -1, 11), new Among("iste", -1, 1),
              new Among("ive", -1, 8), new Among("if", -1, 8),
              new Among("usion", -1, 4), new Among("ation", -1, 2),
              new Among("ution", -1, 4), new Among("ateur", -1, 2),
              new Among("iqUes", -1, 1), new Among("atrices", -1, 2),
              new Among("ances", -1, 1), new Among("ences", -1, 5),
              new Among("logies", -1, 3), new Among("ables", -1, 1),
              new Among("ismes", -1, 1), new Among("euses", -1, 11),
              new Among("istes", -1, 1), new Among("ives", -1, 8),
              new Among("ifs", -1, 8), new Among("usions", -1, 4),
              new Among("ations", -1, 2), new Among("utions", -1, 4),
              new Among("ateurs", -1, 2), new Among("ments", -1, 15),
              new Among("ements", 30, 6), new Among("issements", 31, 12),
              new Among("it\u00E9s", -1, 7), new Among("ment", -1, 15),
              new Among("ement", 34, 6), new Among("issement", 35, 12),
              new Among("amment", 34, 13), new Among("emment", 34, 14),
              new Among("aux", -1, 10), new Among("eaux", 39, 9),
              new Among("eux", -1, 1), new Among("it\u00E9", -1, 7)
            ],
            a_5 = [
              new Among("ira", -1, 1), new Among("ie", -1, 1),
              new Among("isse", -1, 1), new Among("issante", -1, 1),
              new Among("i", -1, 1), new Among("irai", 4, 1),
              new Among("ir", -1, 1), new Among("iras", -1, 1),
              new Among("ies", -1, 1), new Among("\u00EEmes", -1, 1),
              new Among("isses", -1, 1), new Among("issantes", -1, 1),
              new Among("\u00EEtes", -1, 1), new Among("is", -1, 1),
              new Among("irais", 13, 1), new Among("issais", 13, 1),
              new Among("irions", -1, 1), new Among("issions", -1, 1),
              new Among("irons", -1, 1), new Among("issons", -1, 1),
              new Among("issants", -1, 1), new Among("it", -1, 1),
              new Among("irait", 21, 1), new Among("issait", 21, 1),
              new Among("issant", -1, 1), new Among("iraIent", -1, 1),
              new Among("issaIent", -1, 1), new Among("irent", -1, 1),
              new Among("issent", -1, 1), new Among("iront", -1, 1),
              new Among("\u00EEt", -1, 1), new Among("iriez", -1, 1),
              new Among("issiez", -1, 1), new Among("irez", -1, 1),
              new Among("issez", -1, 1)
            ],
            a_6 = [new Among("a", -1, 3),
              new Among("era", 0, 2), new Among("asse", -1, 3),
              new Among("ante", -1, 3), new Among("\u00E9e", -1, 2),
              new Among("ai", -1, 3), new Among("erai", 5, 2),
              new Among("er", -1, 2), new Among("as", -1, 3),
              new Among("eras", 8, 2), new Among("\u00E2mes", -1, 3),
              new Among("asses", -1, 3), new Among("antes", -1, 3),
              new Among("\u00E2tes", -1, 3), new Among("\u00E9es", -1, 2),
              new Among("ais", -1, 3), new Among("erais", 15, 2),
              new Among("ions", -1, 1), new Among("erions", 17, 2),
              new Among("assions", 17, 3), new Among("erons", -1, 2),
              new Among("ants", -1, 3), new Among("\u00E9s", -1, 2),
              new Among("ait", -1, 3), new Among("erait", 23, 2),
              new Among("ant", -1, 3), new Among("aIent", -1, 3),
              new Among("eraIent", 26, 2), new Among("\u00E8rent", -1, 2),
              new Among("assent", -1, 3), new Among("eront", -1, 2),
              new Among("\u00E2t", -1, 3), new Among("ez", -1, 2),
              new Among("iez", 32, 2), new Among("eriez", 33, 2),
              new Among("assiez", 33, 3), new Among("erez", 32, 2),
              new Among("\u00E9", -1, 2)
            ],
            a_7 = [new Among("e", -1, 3),
              new Among("I\u00E8re", 0, 2), new Among("i\u00E8re", 0, 2),
              new Among("ion", -1, 1), new Among("Ier", -1, 2),
              new Among("ier", -1, 2), new Among("\u00EB", -1, 4)
            ],
            a_8 = [
              new Among("ell", -1, -1), new Among("eill", -1, -1),
              new Among("enn", -1, -1), new Among("onn", -1, -1),
              new Among("ett", -1, -1)
            ],
            g_v = [17, 65, 16, 1, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 128, 130, 103, 8, 5
            ],
            g_keep_with_s = [1, 65, 20, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128
            ],
            I_p2, I_p1, I_pV, sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function habr1(c1, c2, v_1) {
            if (sbp.eq_s(1, c1)) {
              sbp.ket = sbp.cursor;
              if (sbp.in_grouping(g_v, 97, 251)) {
                sbp.slice_from(c2);
                sbp.cursor = v_1;
                return true;
              }
            }
            return false;
          }

          function habr2(c1, c2, v_1) {
            if (sbp.eq_s(1, c1)) {
              sbp.ket = sbp.cursor;
              sbp.slice_from(c2);
              sbp.cursor = v_1;
              return true;
            }
            return false;
          }

          function r_prelude() {
            var v_1, v_2;
            while (true) {
              v_1 = sbp.cursor;
              if (sbp.in_grouping(g_v, 97, 251)) {
                sbp.bra = sbp.cursor;
                v_2 = sbp.cursor;
                if (habr1("u", "U", v_1))
                  continue;
                sbp.cursor = v_2;
                if (habr1("i", "I", v_1))
                  continue;
                sbp.cursor = v_2;
                if (habr2("y", "Y", v_1))
                  continue;
              }
              sbp.cursor = v_1;
              sbp.bra = v_1;
              if (!habr1("y", "Y", v_1)) {
                sbp.cursor = v_1;
                if (sbp.eq_s(1, "q")) {
                  sbp.bra = sbp.cursor;
                  if (habr2("u", "U", v_1))
                    continue;
                }
                sbp.cursor = v_1;
                if (v_1 >= sbp.limit)
                  return;
                sbp.cursor++;
              }
            }
          }

          function habr3() {
            while (!sbp.in_grouping(g_v, 97, 251)) {
              if (sbp.cursor >= sbp.limit)
                return true;
              sbp.cursor++;
            }
            while (!sbp.out_grouping(g_v, 97, 251)) {
              if (sbp.cursor >= sbp.limit)
                return true;
              sbp.cursor++;
            }
            return false;
          }

          function r_mark_regions() {
            var v_1 = sbp.cursor;
            I_pV = sbp.limit;
            I_p1 = I_pV;
            I_p2 = I_pV;
            if (sbp.in_grouping(g_v, 97, 251) && sbp.in_grouping(g_v, 97, 251) &&
              sbp.cursor < sbp.limit)
              sbp.cursor++;
            else {
              sbp.cursor = v_1;
              if (!sbp.find_among(a_0, 3)) {
                sbp.cursor = v_1;
                do {
                  if (sbp.cursor >= sbp.limit) {
                    sbp.cursor = I_pV;
                    break;
                  }
                  sbp.cursor++;
                } while (!sbp.in_grouping(g_v, 97, 251));
              }
            }
            I_pV = sbp.cursor;
            sbp.cursor = v_1;
            if (!habr3()) {
              I_p1 = sbp.cursor;
              if (!habr3())
                I_p2 = sbp.cursor;
            }
          }

          function r_postlude() {
            var among_var, v_1;
            while (true) {
              v_1 = sbp.cursor;
              sbp.bra = v_1;
              among_var = sbp.find_among(a_1, 4);
              if (!among_var)
                break;
              sbp.ket = sbp.cursor;
              switch (among_var) {
                case 1:
                  sbp.slice_from("i");
                  break;
                case 2:
                  sbp.slice_from("u");
                  break;
                case 3:
                  sbp.slice_from("y");
                  break;
                case 4:
                  if (sbp.cursor >= sbp.limit)
                    return;
                  sbp.cursor++;
                  break;
              }
            }
          }

          function r_RV() {
            return I_pV <= sbp.cursor;
          }

          function r_R1() {
            return I_p1 <= sbp.cursor;
          }

          function r_R2() {
            return I_p2 <= sbp.cursor;
          }

          function r_standard_suffix() {
            var among_var, v_1;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_4, 43);
            if (among_var) {
              sbp.bra = sbp.cursor;
              switch (among_var) {
                case 1:
                  if (!r_R2())
                    return false;
                  sbp.slice_del();
                  break;
                case 2:
                  if (!r_R2())
                    return false;
                  sbp.slice_del();
                  sbp.ket = sbp.cursor;
                  if (sbp.eq_s_b(2, "ic")) {
                    sbp.bra = sbp.cursor;
                    if (!r_R2())
                      sbp.slice_from("iqU");
                    else
                      sbp.slice_del();
                  }
                  break;
                case 3:
                  if (!r_R2())
                    return false;
                  sbp.slice_from("log");
                  break;
                case 4:
                  if (!r_R2())
                    return false;
                  sbp.slice_from("u");
                  break;
                case 5:
                  if (!r_R2())
                    return false;
                  sbp.slice_from("ent");
                  break;
                case 6:
                  if (!r_RV())
                    return false;
                  sbp.slice_del();
                  sbp.ket = sbp.cursor;
                  among_var = sbp.find_among_b(a_2, 6);
                  if (among_var) {
                    sbp.bra = sbp.cursor;
                    switch (among_var) {
                      case 1:
                        if (r_R2()) {
                          sbp.slice_del();
                          sbp.ket = sbp.cursor;
                          if (sbp.eq_s_b(2, "at")) {
                            sbp.bra = sbp.cursor;
                            if (r_R2())
                              sbp.slice_del();
                          }
                        }
                        break;
                      case 2:
                        if (r_R2())
                          sbp.slice_del();
                        else if (r_R1())
                          sbp.slice_from("eux");
                        break;
                      case 3:
                        if (r_R2())
                          sbp.slice_del();
                        break;
                      case 4:
                        if (r_RV())
                          sbp.slice_from("i");
                        break;
                    }
                  }
                  break;
                case 7:
                  if (!r_R2())
                    return false;
                  sbp.slice_del();
                  sbp.ket = sbp.cursor;
                  among_var = sbp.find_among_b(a_3, 3);
                  if (among_var) {
                    sbp.bra = sbp.cursor;
                    switch (among_var) {
                      case 1:
                        if (r_R2())
                          sbp.slice_del();
                        else
                          sbp.slice_from("abl");
                        break;
                      case 2:
                        if (r_R2())
                          sbp.slice_del();
                        else
                          sbp.slice_from("iqU");
                        break;
                      case 3:
                        if (r_R2())
                          sbp.slice_del();
                        break;
                    }
                  }
                  break;
                case 8:
                  if (!r_R2())
                    return false;
                  sbp.slice_del();
                  sbp.ket = sbp.cursor;
                  if (sbp.eq_s_b(2, "at")) {
                    sbp.bra = sbp.cursor;
                    if (r_R2()) {
                      sbp.slice_del();
                      sbp.ket = sbp.cursor;
                      if (sbp.eq_s_b(2, "ic")) {
                        sbp.bra = sbp.cursor;
                        if (r_R2())
                          sbp.slice_del();
                        else
                          sbp.slice_from("iqU");
                        break;
                      }
                    }
                  }
                  break;
                case 9:
                  sbp.slice_from("eau");
                  break;
                case 10:
                  if (!r_R1())
                    return false;
                  sbp.slice_from("al");
                  break;
                case 11:
                  if (r_R2())
                    sbp.slice_del();
                  else if (!r_R1())
                    return false;
                  else
                    sbp.slice_from("eux");
                  break;
                case 12:
                  if (!r_R1() || !sbp.out_grouping_b(g_v, 97, 251))
                    return false;
                  sbp.slice_del();
                  break;
                case 13:
                  if (r_RV())
                    sbp.slice_from("ant");
                  return false;
                case 14:
                  if (r_RV())
                    sbp.slice_from("ent");
                  return false;
                case 15:
                  v_1 = sbp.limit - sbp.cursor;
                  if (sbp.in_grouping_b(g_v, 97, 251) && r_RV()) {
                    sbp.cursor = sbp.limit - v_1;
                    sbp.slice_del();
                  }
                  return false;
              }
              return true;
            }
            return false;
          }

          function r_i_verb_suffix() {
            var among_var, v_1;
            if (sbp.cursor < I_pV)
              return false;
            v_1 = sbp.limit_backward;
            sbp.limit_backward = I_pV;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_5, 35);
            if (!among_var) {
              sbp.limit_backward = v_1;
              return false;
            }
            sbp.bra = sbp.cursor;
            if (among_var == 1) {
              if (!sbp.out_grouping_b(g_v, 97, 251)) {
                sbp.limit_backward = v_1;
                return false;
              }
              sbp.slice_del();
            }
            sbp.limit_backward = v_1;
            return true;
          }

          function r_verb_suffix() {
            var among_var, v_2, v_3;
            if (sbp.cursor < I_pV)
              return false;
            v_2 = sbp.limit_backward;
            sbp.limit_backward = I_pV;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_6, 38);
            if (!among_var) {
              sbp.limit_backward = v_2;
              return false;
            }
            sbp.bra = sbp.cursor;
            switch (among_var) {
              case 1:
                if (!r_R2()) {
                  sbp.limit_backward = v_2;
                  return false;
                }
                sbp.slice_del();
                break;
              case 2:
                sbp.slice_del();
                break;
              case 3:
                sbp.slice_del();
                v_3 = sbp.limit - sbp.cursor;
                sbp.ket = sbp.cursor;
                if (sbp.eq_s_b(1, "e")) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                } else
                  sbp.cursor = sbp.limit - v_3;
                break;
            }
            sbp.limit_backward = v_2;
            return true;
          }

          function r_residual_suffix() {
            var among_var, v_1 = sbp.limit - sbp.cursor,
              v_2, v_4, v_5;
            sbp.ket = sbp.cursor;
            if (sbp.eq_s_b(1, "s")) {
              sbp.bra = sbp.cursor;
              v_2 = sbp.limit - sbp.cursor;
              if (sbp.out_grouping_b(g_keep_with_s, 97, 232)) {
                sbp.cursor = sbp.limit - v_2;
                sbp.slice_del();
              } else
                sbp.cursor = sbp.limit - v_1;
            } else
              sbp.cursor = sbp.limit - v_1;
            if (sbp.cursor >= I_pV) {
              v_4 = sbp.limit_backward;
              sbp.limit_backward = I_pV;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_7, 7);
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    if (r_R2()) {
                      v_5 = sbp.limit - sbp.cursor;
                      if (!sbp.eq_s_b(1, "s")) {
                        sbp.cursor = sbp.limit - v_5;
                        if (!sbp.eq_s_b(1, "t"))
                          break;
                      }
                      sbp.slice_del();
                    }
                    break;
                  case 2:
                    sbp.slice_from("i");
                    break;
                  case 3:
                    sbp.slice_del();
                    break;
                  case 4:
                    if (sbp.eq_s_b(2, "gu"))
                      sbp.slice_del();
                    break;
                }
              }
              sbp.limit_backward = v_4;
            }
          }

          function r_un_double() {
            var v_1 = sbp.limit - sbp.cursor;
            if (sbp.find_among_b(a_8, 5)) {
              sbp.cursor = sbp.limit - v_1;
              sbp.ket = sbp.cursor;
              if (sbp.cursor > sbp.limit_backward) {
                sbp.cursor--;
                sbp.bra = sbp.cursor;
                sbp.slice_del();
              }
            }
          }

          function r_un_accent() {
            var v_1, v_2 = 1;
            while (sbp.out_grouping_b(g_v, 97, 251))
              v_2--;
            if (v_2 <= 0) {
              sbp.ket = sbp.cursor;
              v_1 = sbp.limit - sbp.cursor;
              if (!sbp.eq_s_b(1, "\u00E9")) {
                sbp.cursor = sbp.limit - v_1;
                if (!sbp.eq_s_b(1, "\u00E8"))
                  return;
              }
              sbp.bra = sbp.cursor;
              sbp.slice_from("e");
            }
          }

          function habr5() {
            if (!r_standard_suffix()) {
              sbp.cursor = sbp.limit;
              if (!r_i_verb_suffix()) {
                sbp.cursor = sbp.limit;
                if (!r_verb_suffix()) {
                  sbp.cursor = sbp.limit;
                  r_residual_suffix();
                  return;
                }
              }
            }
            sbp.cursor = sbp.limit;
            sbp.ket = sbp.cursor;
            if (sbp.eq_s_b(1, "Y")) {
              sbp.bra = sbp.cursor;
              sbp.slice_from("i");
            } else {
              sbp.cursor = sbp.limit;
              if (sbp.eq_s_b(1, "\u00E7")) {
                sbp.bra = sbp.cursor;
                sbp.slice_from("c");
              }
            }
          }
          this.stem = function() {
            var v_1 = sbp.cursor;
            r_prelude();
            sbp.cursor = v_1;
            r_mark_regions();
            sbp.limit_backward = v_1;
            sbp.cursor = sbp.limit;
            habr5();
            sbp.cursor = sbp.limit;
            r_un_double();
            sbp.cursor = sbp.limit;
            r_un_accent();
            sbp.cursor = sbp.limit_backward;
            r_postlude();
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

    lunr.Pipeline.registerFunction(lunr.fr.stemmer, 'stemmer-fr');

    lunr.fr.stopWordFilter = lunr.generateStopWordFilter('ai aie aient aies ait as au aura aurai auraient aurais aurait auras aurez auriez aurions aurons auront aux avaient avais avait avec avez aviez avions avons ayant ayez ayons c ce ceci celà ces cet cette d dans de des du elle en es est et eu eue eues eurent eus eusse eussent eusses eussiez eussions eut eux eûmes eût eûtes furent fus fusse fussent fusses fussiez fussions fut fûmes fût fûtes ici il ils j je l la le les leur leurs lui m ma mais me mes moi mon même n ne nos notre nous on ont ou par pas pour qu que quel quelle quelles quels qui s sa sans se sera serai seraient serais serait seras serez seriez serions serons seront ses soi soient sois soit sommes son sont soyez soyons suis sur t ta te tes toi ton tu un une vos votre vous y à étaient étais était étant étiez étions été étée étées étés êtes'.split(' '));

    lunr.Pipeline.registerFunction(lunr.fr.stopWordFilter, 'stopWordFilter-fr');
  };
}))
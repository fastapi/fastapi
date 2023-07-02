/*!
 * Lunr languages, `Turkish` language
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
    lunr.tr = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.tr.trimmer,
        lunr.tr.stopWordFilter,
        lunr.tr.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.tr.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.tr.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.tr.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.tr.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.tr.trimmer, 'trimmer-tr');

    /* lunr stemmer function */
    lunr.tr.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function TurkishStemmer() {
          var a_0 = [new Among("m", -1, -1), new Among("n", -1, -1),
              new Among("miz", -1, -1), new Among("niz", -1, -1),
              new Among("muz", -1, -1), new Among("nuz", -1, -1),
              new Among("m\u00FCz", -1, -1), new Among("n\u00FCz", -1, -1),
              new Among("m\u0131z", -1, -1), new Among("n\u0131z", -1, -1)
            ],
            a_1 = [
              new Among("leri", -1, -1), new Among("lar\u0131", -1, -1)
            ],
            a_2 = [
              new Among("ni", -1, -1), new Among("nu", -1, -1),
              new Among("n\u00FC", -1, -1), new Among("n\u0131", -1, -1)
            ],
            a_3 = [
              new Among("in", -1, -1), new Among("un", -1, -1),
              new Among("\u00FCn", -1, -1), new Among("\u0131n", -1, -1)
            ],
            a_4 = [
              new Among("a", -1, -1), new Among("e", -1, -1)
            ],
            a_5 = [
              new Among("na", -1, -1), new Among("ne", -1, -1)
            ],
            a_6 = [
              new Among("da", -1, -1), new Among("ta", -1, -1),
              new Among("de", -1, -1), new Among("te", -1, -1)
            ],
            a_7 = [
              new Among("nda", -1, -1), new Among("nde", -1, -1)
            ],
            a_8 = [
              new Among("dan", -1, -1), new Among("tan", -1, -1),
              new Among("den", -1, -1), new Among("ten", -1, -1)
            ],
            a_9 = [
              new Among("ndan", -1, -1), new Among("nden", -1, -1)
            ],
            a_10 = [
              new Among("la", -1, -1), new Among("le", -1, -1)
            ],
            a_11 = [
              new Among("ca", -1, -1), new Among("ce", -1, -1)
            ],
            a_12 = [
              new Among("im", -1, -1), new Among("um", -1, -1),
              new Among("\u00FCm", -1, -1), new Among("\u0131m", -1, -1)
            ],
            a_13 = [
              new Among("sin", -1, -1), new Among("sun", -1, -1),
              new Among("s\u00FCn", -1, -1), new Among("s\u0131n", -1, -1)
            ],
            a_14 = [
              new Among("iz", -1, -1), new Among("uz", -1, -1),
              new Among("\u00FCz", -1, -1), new Among("\u0131z", -1, -1)
            ],
            a_15 = [
              new Among("siniz", -1, -1), new Among("sunuz", -1, -1),
              new Among("s\u00FCn\u00FCz", -1, -1),
              new Among("s\u0131n\u0131z", -1, -1)
            ],
            a_16 = [
              new Among("lar", -1, -1), new Among("ler", -1, -1)
            ],
            a_17 = [
              new Among("niz", -1, -1), new Among("nuz", -1, -1),
              new Among("n\u00FCz", -1, -1), new Among("n\u0131z", -1, -1)
            ],
            a_18 = [
              new Among("dir", -1, -1), new Among("tir", -1, -1),
              new Among("dur", -1, -1), new Among("tur", -1, -1),
              new Among("d\u00FCr", -1, -1), new Among("t\u00FCr", -1, -1),
              new Among("d\u0131r", -1, -1), new Among("t\u0131r", -1, -1)
            ],
            a_19 = [
              new Among("cas\u0131na", -1, -1), new Among("cesine", -1, -1)
            ],
            a_20 = [
              new Among("di", -1, -1), new Among("ti", -1, -1),
              new Among("dik", -1, -1), new Among("tik", -1, -1),
              new Among("duk", -1, -1), new Among("tuk", -1, -1),
              new Among("d\u00FCk", -1, -1), new Among("t\u00FCk", -1, -1),
              new Among("d\u0131k", -1, -1), new Among("t\u0131k", -1, -1),
              new Among("dim", -1, -1), new Among("tim", -1, -1),
              new Among("dum", -1, -1), new Among("tum", -1, -1),
              new Among("d\u00FCm", -1, -1), new Among("t\u00FCm", -1, -1),
              new Among("d\u0131m", -1, -1), new Among("t\u0131m", -1, -1),
              new Among("din", -1, -1), new Among("tin", -1, -1),
              new Among("dun", -1, -1), new Among("tun", -1, -1),
              new Among("d\u00FCn", -1, -1), new Among("t\u00FCn", -1, -1),
              new Among("d\u0131n", -1, -1), new Among("t\u0131n", -1, -1),
              new Among("du", -1, -1), new Among("tu", -1, -1),
              new Among("d\u00FC", -1, -1), new Among("t\u00FC", -1, -1),
              new Among("d\u0131", -1, -1), new Among("t\u0131", -1, -1)
            ],
            a_21 = [
              new Among("sa", -1, -1), new Among("se", -1, -1),
              new Among("sak", -1, -1), new Among("sek", -1, -1),
              new Among("sam", -1, -1), new Among("sem", -1, -1),
              new Among("san", -1, -1), new Among("sen", -1, -1)
            ],
            a_22 = [
              new Among("mi\u015F", -1, -1), new Among("mu\u015F", -1, -1),
              new Among("m\u00FC\u015F", -1, -1),
              new Among("m\u0131\u015F", -1, -1)
            ],
            a_23 = [new Among("b", -1, 1),
              new Among("c", -1, 2), new Among("d", -1, 3),
              new Among("\u011F", -1, 4)
            ],
            g_vowel = [17, 65, 16, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 8, 0, 0, 0, 0, 0, 0, 1
            ],
            g_U = [
              1, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0,
              0, 0, 0, 1
            ],
            g_vowel1 = [1, 64, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
            ],
            g_vowel2 = [17, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 130
            ],
            g_vowel3 = [1, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 1
            ],
            g_vowel4 = [17],
            g_vowel5 = [65],
            g_vowel6 = [65],
            B_c_s_n_s, I_strlen, g_habr = [
              ["a", g_vowel1, 97, 305],
              ["e", g_vowel2, 101, 252],
              ["\u0131", g_vowel3, 97, 305],
              ["i", g_vowel4, 101, 105],
              ["o", g_vowel5, 111, 117],
              ["\u00F6", g_vowel6, 246, 252],
              ["u", g_vowel5, 111, 117]
            ],
            sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function habr1(g_v, n1, n2) {
            while (true) {
              var v_1 = sbp.limit - sbp.cursor;
              if (sbp.in_grouping_b(g_v, n1, n2)) {
                sbp.cursor = sbp.limit - v_1;
                break;
              }
              sbp.cursor = sbp.limit - v_1;
              if (sbp.cursor <= sbp.limit_backward)
                return false;
              sbp.cursor--;
            }
            return true;
          }

          function r_check_vowel_harmony() {
            var v_1, v_2;
            v_1 = sbp.limit - sbp.cursor;
            habr1(g_vowel, 97, 305);
            for (var i = 0; i < g_habr.length; i++) {
              v_2 = sbp.limit - sbp.cursor;
              var habr = g_habr[i];
              if (sbp.eq_s_b(1, habr[0]) && habr1(habr[1], habr[2], habr[3])) {
                sbp.cursor = sbp.limit - v_1;
                return true;
              }
              sbp.cursor = sbp.limit - v_2;
            }
            sbp.cursor = sbp.limit - v_2;
            if (!sbp.eq_s_b(1, "\u00FC") || !habr1(g_vowel6, 246, 252))
              return false;
            sbp.cursor = sbp.limit - v_1;
            return true;
          }

          function habr2(f1, f2) {
            var v_1 = sbp.limit - sbp.cursor,
              v_2;
            if (f1()) {
              sbp.cursor = sbp.limit - v_1;
              if (sbp.cursor > sbp.limit_backward) {
                sbp.cursor--;
                v_2 = sbp.limit - sbp.cursor;
                if (f2()) {
                  sbp.cursor = sbp.limit - v_2;
                  return true;
                }
              }
            }
            sbp.cursor = sbp.limit - v_1;
            if (f1()) {
              sbp.cursor = sbp.limit - v_1;
              return false;
            }
            sbp.cursor = sbp.limit - v_1;
            if (sbp.cursor <= sbp.limit_backward)
              return false;
            sbp.cursor--;
            if (!f2())
              return false;
            sbp.cursor = sbp.limit - v_1;
            return true;
          }

          function habr3(f1) {
            return habr2(f1, function() {
              return sbp.in_grouping_b(g_vowel, 97, 305);
            });
          }

          function r_mark_suffix_with_optional_n_consonant() {
            return habr3(function() {
              return sbp.eq_s_b(1, "n");
            });
          }

          function r_mark_suffix_with_optional_s_consonant() {
            return habr3(function() {
              return sbp.eq_s_b(1, "s");
            });
          }

          function r_mark_suffix_with_optional_y_consonant() {
            return habr3(function() {
              return sbp.eq_s_b(1, "y");
            });
          }

          function r_mark_suffix_with_optional_U_vowel() {
            return habr2(function() {
              return sbp.in_grouping_b(g_U, 105, 305);
            }, function() {
              return sbp.out_grouping_b(g_vowel, 97, 305);
            });
          }

          function r_mark_possessives() {
            return sbp.find_among_b(a_0, 10) &&
              r_mark_suffix_with_optional_U_vowel();
          }

          function r_mark_sU() {
            return r_check_vowel_harmony() && sbp.in_grouping_b(g_U, 105, 305) &&
              r_mark_suffix_with_optional_s_consonant();
          }

          function r_mark_lArI() {
            return sbp.find_among_b(a_1, 2);
          }

          function r_mark_yU() {
            return r_check_vowel_harmony() && sbp.in_grouping_b(g_U, 105, 305) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_nU() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_2, 4);
          }

          function r_mark_nUn() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_3, 4) &&
              r_mark_suffix_with_optional_n_consonant();
          }

          function r_mark_yA() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_4, 2) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_nA() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_5, 2);
          }

          function r_mark_DA() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_6, 4);
          }

          function r_mark_ndA() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_7, 2);
          }

          function r_mark_DAn() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_8, 4);
          }

          function r_mark_ndAn() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_9, 2);
          }

          function r_mark_ylA() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_10, 2) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_ki() {
            return sbp.eq_s_b(2, "ki");
          }

          function r_mark_ncA() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_11, 2) &&
              r_mark_suffix_with_optional_n_consonant();
          }

          function r_mark_yUm() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_12, 4) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_sUn() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_13, 4);
          }

          function r_mark_yUz() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_14, 4) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_sUnUz() {
            return sbp.find_among_b(a_15, 4);
          }

          function r_mark_lAr() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_16, 2);
          }

          function r_mark_nUz() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_17, 4);
          }

          function r_mark_DUr() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_18, 8);
          }

          function r_mark_cAsInA() {
            return sbp.find_among_b(a_19, 2);
          }

          function r_mark_yDU() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_20, 32) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_ysA() {
            return sbp.find_among_b(a_21, 8) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_ymUs_() {
            return r_check_vowel_harmony() && sbp.find_among_b(a_22, 4) &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function r_mark_yken() {
            return sbp.eq_s_b(3, "ken") &&
              r_mark_suffix_with_optional_y_consonant();
          }

          function habr4() {
            var v_1 = sbp.limit - sbp.cursor;
            if (!r_mark_ymUs_()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_yDU()) {
                sbp.cursor = sbp.limit - v_1;
                if (!r_mark_ysA()) {
                  sbp.cursor = sbp.limit - v_1;
                  if (!r_mark_yken())
                    return true;
                }
              }
            }
            return false;
          }

          function habr5() {
            if (r_mark_cAsInA()) {
              var v_1 = sbp.limit - sbp.cursor;
              if (!r_mark_sUnUz()) {
                sbp.cursor = sbp.limit - v_1;
                if (!r_mark_lAr()) {
                  sbp.cursor = sbp.limit - v_1;
                  if (!r_mark_yUm()) {
                    sbp.cursor = sbp.limit - v_1;
                    if (!r_mark_sUn()) {
                      sbp.cursor = sbp.limit - v_1;
                      if (!r_mark_yUz())
                        sbp.cursor = sbp.limit - v_1;
                    }
                  }
                }
              }
              if (r_mark_ymUs_())
                return false;
            }
            return true;
          }

          function habr6() {
            if (r_mark_lAr()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              var v_1 = sbp.limit - sbp.cursor;
              sbp.ket = sbp.cursor;
              if (!r_mark_DUr()) {
                sbp.cursor = sbp.limit - v_1;
                if (!r_mark_yDU()) {
                  sbp.cursor = sbp.limit - v_1;
                  if (!r_mark_ysA()) {
                    sbp.cursor = sbp.limit - v_1;
                    if (!r_mark_ymUs_())
                      sbp.cursor = sbp.limit - v_1;
                  }
                }
              }
              B_c_s_n_s = false;
              return false;
            }
            return true;
          }

          function habr7() {
            if (!r_mark_nUz())
              return true;
            var v_1 = sbp.limit - sbp.cursor;
            if (!r_mark_yDU()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_ysA())
                return true;
            }
            return false;
          }

          function habr8() {
            var v_1 = sbp.limit - sbp.cursor,
              v_2;
            if (!r_mark_sUnUz()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_yUz()) {
                sbp.cursor = sbp.limit - v_1;
                if (!r_mark_sUn()) {
                  sbp.cursor = sbp.limit - v_1;
                  if (!r_mark_yUm())
                    return true;
                }
              }
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            v_2 = sbp.limit - sbp.cursor;
            sbp.ket = sbp.cursor;
            if (!r_mark_ymUs_())
              sbp.cursor = sbp.limit - v_2;
            return false;
          }

          function r_stem_nominal_verb_suffixes() {
            var v_1 = sbp.limit - sbp.cursor,
              v_2;
            sbp.ket = sbp.cursor;
            B_c_s_n_s = true;
            if (habr4()) {
              sbp.cursor = sbp.limit - v_1;
              if (habr5()) {
                sbp.cursor = sbp.limit - v_1;
                if (habr6()) {
                  sbp.cursor = sbp.limit - v_1;
                  if (habr7()) {
                    sbp.cursor = sbp.limit - v_1;
                    if (habr8()) {
                      sbp.cursor = sbp.limit - v_1;
                      if (!r_mark_DUr())
                        return;
                      sbp.bra = sbp.cursor;
                      sbp.slice_del();
                      sbp.ket = sbp.cursor;
                      v_2 = sbp.limit - sbp.cursor;
                      if (!r_mark_sUnUz()) {
                        sbp.cursor = sbp.limit - v_2;
                        if (!r_mark_lAr()) {
                          sbp.cursor = sbp.limit - v_2;
                          if (!r_mark_yUm()) {
                            sbp.cursor = sbp.limit - v_2;
                            if (!r_mark_sUn()) {
                              sbp.cursor = sbp.limit - v_2;
                              if (!r_mark_yUz())
                                sbp.cursor = sbp.limit - v_2;
                            }
                          }
                        }
                      }
                      if (!r_mark_ymUs_())
                        sbp.cursor = sbp.limit - v_2;
                    }
                  }
                }
              }
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
          }

          function r_stem_suffix_chain_before_ki() {
            var v_1, v_2, v_3, v_4;
            sbp.ket = sbp.cursor;
            if (r_mark_ki()) {
              v_1 = sbp.limit - sbp.cursor;
              if (r_mark_DA()) {
                sbp.bra = sbp.cursor;
                sbp.slice_del();
                v_2 = sbp.limit - sbp.cursor;
                sbp.ket = sbp.cursor;
                if (r_mark_lAr()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                  r_stem_suffix_chain_before_ki();
                } else {
                  sbp.cursor = sbp.limit - v_2;
                  if (r_mark_possessives()) {
                    sbp.bra = sbp.cursor;
                    sbp.slice_del();
                    sbp.ket = sbp.cursor;
                    if (r_mark_lAr()) {
                      sbp.bra = sbp.cursor;
                      sbp.slice_del();
                      r_stem_suffix_chain_before_ki();
                    }
                  }
                }
                return true;
              }
              sbp.cursor = sbp.limit - v_1;
              if (r_mark_nUn()) {
                sbp.bra = sbp.cursor;
                sbp.slice_del();
                sbp.ket = sbp.cursor;
                v_3 = sbp.limit - sbp.cursor;
                if (r_mark_lArI()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                } else {
                  sbp.cursor = sbp.limit - v_3;
                  sbp.ket = sbp.cursor;
                  if (!r_mark_possessives()) {
                    sbp.cursor = sbp.limit - v_3;
                    if (!r_mark_sU()) {
                      sbp.cursor = sbp.limit - v_3;
                      if (!r_stem_suffix_chain_before_ki())
                        return true;
                    }
                  }
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                  sbp.ket = sbp.cursor;
                  if (r_mark_lAr()) {
                    sbp.bra = sbp.cursor;
                    sbp.slice_del();
                    r_stem_suffix_chain_before_ki()
                  }
                }
                return true;
              }
              sbp.cursor = sbp.limit - v_1;
              if (r_mark_ndA()) {
                v_4 = sbp.limit - sbp.cursor;
                if (r_mark_lArI()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                } else {
                  sbp.cursor = sbp.limit - v_4;
                  if (r_mark_sU()) {
                    sbp.bra = sbp.cursor;
                    sbp.slice_del();
                    sbp.ket = sbp.cursor;
                    if (r_mark_lAr()) {
                      sbp.bra = sbp.cursor;
                      sbp.slice_del();
                      r_stem_suffix_chain_before_ki();
                    }
                  } else {
                    sbp.cursor = sbp.limit - v_4;
                    if (!r_stem_suffix_chain_before_ki())
                      return false;
                  }
                }
                return true;
              }
            }
            return false;
          }

          function habr9(v_1) {
            sbp.ket = sbp.cursor;
            if (!r_mark_ndA()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_nA())
                return false;
            }
            var v_2 = sbp.limit - sbp.cursor;
            if (r_mark_lArI()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
            } else {
              sbp.cursor = sbp.limit - v_2;
              if (r_mark_sU()) {
                sbp.bra = sbp.cursor;
                sbp.slice_del();
                sbp.ket = sbp.cursor;
                if (r_mark_lAr()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                  r_stem_suffix_chain_before_ki();
                }
              } else {
                sbp.cursor = sbp.limit - v_2;
                if (!r_stem_suffix_chain_before_ki())
                  return false;
              }
            }
            return true;
          }

          function habr10(v_1) {
            sbp.ket = sbp.cursor;
            if (!r_mark_ndAn()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_nU())
                return false;
            }
            var v_2 = sbp.limit - sbp.cursor;
            if (!r_mark_sU()) {
              sbp.cursor = sbp.limit - v_2;
              if (!r_mark_lArI())
                return false;
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            sbp.ket = sbp.cursor;
            if (r_mark_lAr()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              r_stem_suffix_chain_before_ki();
            }
            return true;
          }

          function habr11() {
            var v_1 = sbp.limit - sbp.cursor,
              v_2;
            sbp.ket = sbp.cursor;
            if (!r_mark_nUn()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_ylA())
                return false;
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            v_2 = sbp.limit - sbp.cursor;
            sbp.ket = sbp.cursor;
            if (r_mark_lAr()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              if (r_stem_suffix_chain_before_ki())
                return true;
            }
            sbp.cursor = sbp.limit - v_2;
            sbp.ket = sbp.cursor;
            if (!r_mark_possessives()) {
              sbp.cursor = sbp.limit - v_2;
              if (!r_mark_sU()) {
                sbp.cursor = sbp.limit - v_2;
                if (!r_stem_suffix_chain_before_ki())
                  return true;
              }
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            sbp.ket = sbp.cursor;
            if (r_mark_lAr()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              r_stem_suffix_chain_before_ki();
            }
            return true;
          }

          function habr12() {
            var v_1 = sbp.limit - sbp.cursor,
              v_2, v_3;
            sbp.ket = sbp.cursor;
            if (!r_mark_DA()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_yU()) {
                sbp.cursor = sbp.limit - v_1;
                if (!r_mark_yA())
                  return false;
              }
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            sbp.ket = sbp.cursor;
            v_2 = sbp.limit - sbp.cursor;
            if (r_mark_possessives()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              v_3 = sbp.limit - sbp.cursor;
              sbp.ket = sbp.cursor;
              if (!r_mark_lAr())
                sbp.cursor = sbp.limit - v_3;
            } else {
              sbp.cursor = sbp.limit - v_2;
              if (!r_mark_lAr())
                return true;
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            sbp.ket = sbp.cursor;
            r_stem_suffix_chain_before_ki();
            return true;
          }

          function r_stem_noun_suffixes() {
            var v_1 = sbp.limit - sbp.cursor,
              v_2, v_3;
            sbp.ket = sbp.cursor;
            if (r_mark_lAr()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              r_stem_suffix_chain_before_ki();
              return;
            }
            sbp.cursor = sbp.limit - v_1;
            sbp.ket = sbp.cursor;
            if (r_mark_ncA()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              v_2 = sbp.limit - sbp.cursor;
              sbp.ket = sbp.cursor;
              if (r_mark_lArI()) {
                sbp.bra = sbp.cursor;
                sbp.slice_del();
              } else {
                sbp.cursor = sbp.limit - v_2;
                sbp.ket = sbp.cursor;
                if (!r_mark_possessives()) {
                  sbp.cursor = sbp.limit - v_2;
                  if (!r_mark_sU()) {
                    sbp.cursor = sbp.limit - v_2;
                    sbp.ket = sbp.cursor;
                    if (!r_mark_lAr())
                      return;
                    sbp.bra = sbp.cursor;
                    sbp.slice_del();
                    if (!r_stem_suffix_chain_before_ki())
                      return;
                  }
                }
                sbp.bra = sbp.cursor;
                sbp.slice_del();
                sbp.ket = sbp.cursor;
                if (r_mark_lAr()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                  r_stem_suffix_chain_before_ki();
                }
              }
              return;
            }
            sbp.cursor = sbp.limit - v_1;
            if (habr9(v_1))
              return;
            sbp.cursor = sbp.limit - v_1;
            if (habr10(v_1))
              return;
            sbp.cursor = sbp.limit - v_1;
            sbp.ket = sbp.cursor;
            if (r_mark_DAn()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              sbp.ket = sbp.cursor;
              v_3 = sbp.limit - sbp.cursor;
              if (r_mark_possessives()) {
                sbp.bra = sbp.cursor;
                sbp.slice_del();
                sbp.ket = sbp.cursor;
                if (r_mark_lAr()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                  r_stem_suffix_chain_before_ki();
                }
              } else {
                sbp.cursor = sbp.limit - v_3;
                if (r_mark_lAr()) {
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                  r_stem_suffix_chain_before_ki();
                } else {
                  sbp.cursor = sbp.limit - v_3;
                  r_stem_suffix_chain_before_ki();
                }
              }
              return;
            }
            sbp.cursor = sbp.limit - v_1;
            if (habr11())
              return;
            sbp.cursor = sbp.limit - v_1;
            if (r_mark_lArI()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              return;
            }
            sbp.cursor = sbp.limit - v_1;
            if (r_stem_suffix_chain_before_ki())
              return;
            sbp.cursor = sbp.limit - v_1;
            if (habr12())
              return;
            sbp.cursor = sbp.limit - v_1;
            sbp.ket = sbp.cursor;
            if (!r_mark_possessives()) {
              sbp.cursor = sbp.limit - v_1;
              if (!r_mark_sU())
                return;
            }
            sbp.bra = sbp.cursor;
            sbp.slice_del();
            sbp.ket = sbp.cursor;
            if (r_mark_lAr()) {
              sbp.bra = sbp.cursor;
              sbp.slice_del();
              r_stem_suffix_chain_before_ki();
            }
          }

          function r_post_process_last_consonants() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_23, 4);
            if (among_var) {
              sbp.bra = sbp.cursor;
              switch (among_var) {
                case 1:
                  sbp.slice_from("p");
                  break;
                case 2:
                  sbp.slice_from("\u00E7");
                  break;
                case 3:
                  sbp.slice_from("t");
                  break;
                case 4:
                  sbp.slice_from("k");
                  break;
              }
            }
          }

          function habr13() {
            while (true) {
              var v_1 = sbp.limit - sbp.cursor;
              if (sbp.in_grouping_b(g_vowel, 97, 305)) {
                sbp.cursor = sbp.limit - v_1;
                break;
              }
              sbp.cursor = sbp.limit - v_1;
              if (sbp.cursor <= sbp.limit_backward)
                return false;
              sbp.cursor--;
            }
            return true;
          }

          function habr14(v_1, c1, c2) {
            sbp.cursor = sbp.limit - v_1;
            if (habr13()) {
              var v_2 = sbp.limit - sbp.cursor;
              if (!sbp.eq_s_b(1, c1)) {
                sbp.cursor = sbp.limit - v_2;
                if (!sbp.eq_s_b(1, c2))
                  return true;
              }
              sbp.cursor = sbp.limit - v_1;
              var c = sbp.cursor;
              sbp.insert(sbp.cursor, sbp.cursor, c2);
              sbp.cursor = c;
              return false;
            }
            return true;
          }

          function r_append_U_to_stems_ending_with_d_or_g() {
            var v_1 = sbp.limit - sbp.cursor;
            if (!sbp.eq_s_b(1, "d")) {
              sbp.cursor = sbp.limit - v_1;
              if (!sbp.eq_s_b(1, "g"))
                return;
            }
            if (habr14(v_1, "a", "\u0131"))
              if (habr14(v_1, "e", "i"))
                if (habr14(v_1, "o", "u"))
                  habr14(v_1, "\u00F6", "\u00FC")
          }

          function r_more_than_one_syllable_word() {
            var v_1 = sbp.cursor,
              v_2 = 2,
              v_3;
            while (true) {
              v_3 = sbp.cursor;
              while (!sbp.in_grouping(g_vowel, 97, 305)) {
                if (sbp.cursor >= sbp.limit) {
                  sbp.cursor = v_3;
                  if (v_2 > 0)
                    return false;
                  sbp.cursor = v_1;
                  return true;
                }
                sbp.cursor++;
              }
              v_2--;
            }
          }

          function habr15(v_1, n1, c1) {
            while (!sbp.eq_s(n1, c1)) {
              if (sbp.cursor >= sbp.limit)
                return true;
              sbp.cursor++;
            }
            I_strlen = n1;
            if (I_strlen != sbp.limit)
              return true;
            sbp.cursor = v_1;
            return false;
          }

          function r_is_reserved_word() {
            var v_1 = sbp.cursor;
            if (habr15(v_1, 2, "ad")) {
              sbp.cursor = v_1;
              if (habr15(v_1, 5, "soyad"))
                return false;
            }
            return true;
          }

          function r_postlude() {
            var v_1 = sbp.cursor;
            if (r_is_reserved_word())
              return false;
            sbp.limit_backward = v_1;
            sbp.cursor = sbp.limit;
            r_append_U_to_stems_ending_with_d_or_g();
            sbp.cursor = sbp.limit;
            r_post_process_last_consonants();
            return true;
          }
          this.stem = function() {
            if (r_more_than_one_syllable_word()) {
              sbp.limit_backward = sbp.cursor;
              sbp.cursor = sbp.limit;
              r_stem_nominal_verb_suffixes();
              sbp.cursor = sbp.limit;
              if (B_c_s_n_s) {
                r_stem_noun_suffixes();
                sbp.cursor = sbp.limit_backward;
                if (r_postlude())
                  return true;
              }
            }
            return false;
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

    lunr.Pipeline.registerFunction(lunr.tr.stemmer, 'stemmer-tr');

    lunr.tr.stopWordFilter = lunr.generateStopWordFilter('acaba altmış altı ama ancak arada aslında ayrıca bana bazı belki ben benden beni benim beri beş bile bin bir biri birkaç birkez birçok birşey birşeyi biz bizden bize bizi bizim bu buna bunda bundan bunlar bunları bunların bunu bunun burada böyle böylece da daha dahi de defa değil diye diğer doksan dokuz dolayı dolayısıyla dört edecek eden ederek edilecek ediliyor edilmesi ediyor elli en etmesi etti ettiği ettiğini eğer gibi göre halen hangi hatta hem henüz hep hepsi her herhangi herkesin hiç hiçbir iki ile ilgili ise itibaren itibariyle için işte kadar karşın katrilyon kendi kendilerine kendini kendisi kendisine kendisini kez ki kim kimden kime kimi kimse kırk milyar milyon mu mü mı nasıl ne neden nedenle nerde nerede nereye niye niçin o olan olarak oldu olduklarını olduğu olduğunu olmadı olmadığı olmak olması olmayan olmaz olsa olsun olup olur olursa oluyor on ona ondan onlar onlardan onları onların onu onun otuz oysa pek rağmen sadece sanki sekiz seksen sen senden seni senin siz sizden sizi sizin tarafından trilyon tüm var vardı ve veya ya yani yapacak yapmak yaptı yaptıkları yaptığı yaptığını yapılan yapılması yapıyor yedi yerine yetmiş yine yirmi yoksa yüz zaten çok çünkü öyle üzere üç şey şeyden şeyi şeyler şu şuna şunda şundan şunları şunu şöyle'.split(' '));

    lunr.Pipeline.registerFunction(lunr.tr.stopWordFilter, 'stopWordFilter-tr');
  };
}))
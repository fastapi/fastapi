/*!
 * Lunr languages, `Finnish` language
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
    lunr.fi = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.fi.trimmer,
        lunr.fi.stopWordFilter,
        lunr.fi.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.fi.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.fi.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.fi.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.fi.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.fi.trimmer, 'trimmer-fi');

    /* lunr stemmer function */
    lunr.fi.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function FinnishStemmer() {
          var a_0 = [new Among("pa", -1, 1), new Among("sti", -1, 2),
              new Among("kaan", -1, 1), new Among("han", -1, 1),
              new Among("kin", -1, 1), new Among("h\u00E4n", -1, 1),
              new Among("k\u00E4\u00E4n", -1, 1), new Among("ko", -1, 1),
              new Among("p\u00E4", -1, 1), new Among("k\u00F6", -1, 1)
            ],
            a_1 = [
              new Among("lla", -1, -1), new Among("na", -1, -1),
              new Among("ssa", -1, -1), new Among("ta", -1, -1),
              new Among("lta", 3, -1), new Among("sta", 3, -1)
            ],
            a_2 = [
              new Among("ll\u00E4", -1, -1), new Among("n\u00E4", -1, -1),
              new Among("ss\u00E4", -1, -1), new Among("t\u00E4", -1, -1),
              new Among("lt\u00E4", 3, -1), new Among("st\u00E4", 3, -1)
            ],
            a_3 = [
              new Among("lle", -1, -1), new Among("ine", -1, -1)
            ],
            a_4 = [
              new Among("nsa", -1, 3), new Among("mme", -1, 3),
              new Among("nne", -1, 3), new Among("ni", -1, 2),
              new Among("si", -1, 1), new Among("an", -1, 4),
              new Among("en", -1, 6), new Among("\u00E4n", -1, 5),
              new Among("ns\u00E4", -1, 3)
            ],
            a_5 = [new Among("aa", -1, -1),
              new Among("ee", -1, -1), new Among("ii", -1, -1),
              new Among("oo", -1, -1), new Among("uu", -1, -1),
              new Among("\u00E4\u00E4", -1, -1),
              new Among("\u00F6\u00F6", -1, -1)
            ],
            a_6 = [new Among("a", -1, 8),
              new Among("lla", 0, -1), new Among("na", 0, -1),
              new Among("ssa", 0, -1), new Among("ta", 0, -1),
              new Among("lta", 4, -1), new Among("sta", 4, -1),
              new Among("tta", 4, 9), new Among("lle", -1, -1),
              new Among("ine", -1, -1), new Among("ksi", -1, -1),
              new Among("n", -1, 7), new Among("han", 11, 1),
              new Among("den", 11, -1, r_VI), new Among("seen", 11, -1, r_LONG),
              new Among("hen", 11, 2), new Among("tten", 11, -1, r_VI),
              new Among("hin", 11, 3), new Among("siin", 11, -1, r_VI),
              new Among("hon", 11, 4), new Among("h\u00E4n", 11, 5),
              new Among("h\u00F6n", 11, 6), new Among("\u00E4", -1, 8),
              new Among("ll\u00E4", 22, -1), new Among("n\u00E4", 22, -1),
              new Among("ss\u00E4", 22, -1), new Among("t\u00E4", 22, -1),
              new Among("lt\u00E4", 26, -1), new Among("st\u00E4", 26, -1),
              new Among("tt\u00E4", 26, 9)
            ],
            a_7 = [new Among("eja", -1, -1),
              new Among("mma", -1, 1), new Among("imma", 1, -1),
              new Among("mpa", -1, 1), new Among("impa", 3, -1),
              new Among("mmi", -1, 1), new Among("immi", 5, -1),
              new Among("mpi", -1, 1), new Among("impi", 7, -1),
              new Among("ej\u00E4", -1, -1), new Among("mm\u00E4", -1, 1),
              new Among("imm\u00E4", 10, -1), new Among("mp\u00E4", -1, 1),
              new Among("imp\u00E4", 12, -1)
            ],
            a_8 = [new Among("i", -1, -1),
              new Among("j", -1, -1)
            ],
            a_9 = [new Among("mma", -1, 1),
              new Among("imma", 0, -1)
            ],
            g_AEI = [17, 1, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 8
            ],
            g_V1 = [17, 65, 16, 1, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 8, 0, 32
            ],
            g_V2 = [17, 65, 16, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 8, 0, 32
            ],
            g_particle_end = [17, 97, 24, 1, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 32
            ],
            B_ending_removed, S_x, I_p2, I_p1, sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function r_mark_regions() {
            I_p1 = sbp.limit;
            I_p2 = I_p1;
            if (!habr1()) {
              I_p1 = sbp.cursor;
              if (!habr1())
                I_p2 = sbp.cursor;
            }
          }

          function habr1() {
            var v_1;
            while (true) {
              v_1 = sbp.cursor;
              if (sbp.in_grouping(g_V1, 97, 246))
                break;
              sbp.cursor = v_1;
              if (v_1 >= sbp.limit)
                return true;
              sbp.cursor++;
            }
            sbp.cursor = v_1;
            while (!sbp.out_grouping(g_V1, 97, 246)) {
              if (sbp.cursor >= sbp.limit)
                return true;
              sbp.cursor++;
            }
            return false;
          }

          function r_R2() {
            return I_p2 <= sbp.cursor;
          }

          function r_particle_etc() {
            var among_var, v_1;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_0, 10);
              if (among_var) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_1;
                switch (among_var) {
                  case 1:
                    if (!sbp.in_grouping_b(g_particle_end, 97, 246))
                      return;
                    break;
                  case 2:
                    if (!r_R2())
                      return;
                    break;
                }
                sbp.slice_del();
              } else
                sbp.limit_backward = v_1;
            }
          }

          function r_possessive() {
            var among_var, v_1, v_2;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_4, 9);
              if (among_var) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_1;
                switch (among_var) {
                  case 1:
                    v_2 = sbp.limit - sbp.cursor;
                    if (!sbp.eq_s_b(1, "k")) {
                      sbp.cursor = sbp.limit - v_2;
                      sbp.slice_del();
                    }
                    break;
                  case 2:
                    sbp.slice_del();
                    sbp.ket = sbp.cursor;
                    if (sbp.eq_s_b(3, "kse")) {
                      sbp.bra = sbp.cursor;
                      sbp.slice_from("ksi");
                    }
                    break;
                  case 3:
                    sbp.slice_del();
                    break;
                  case 4:
                    if (sbp.find_among_b(a_1, 6))
                      sbp.slice_del();
                    break;
                  case 5:
                    if (sbp.find_among_b(a_2, 6))
                      sbp.slice_del();
                    break;
                  case 6:
                    if (sbp.find_among_b(a_3, 2))
                      sbp.slice_del();
                    break;
                }
              } else
                sbp.limit_backward = v_1;
            }
          }

          function r_LONG() {
            return sbp.find_among_b(a_5, 7);
          }

          function r_VI() {
            return sbp.eq_s_b(1, "i") && sbp.in_grouping_b(g_V2, 97, 246);
          }

          function r_case_ending() {
            var among_var, v_1, v_2;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_6, 30);
              if (among_var) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_1;
                switch (among_var) {
                  case 1:
                    if (!sbp.eq_s_b(1, "a"))
                      return;
                    break;
                  case 2:
                  case 9:
                    if (!sbp.eq_s_b(1, "e"))
                      return;
                    break;
                  case 3:
                    if (!sbp.eq_s_b(1, "i"))
                      return;
                    break;
                  case 4:
                    if (!sbp.eq_s_b(1, "o"))
                      return;
                    break;
                  case 5:
                    if (!sbp.eq_s_b(1, "\u00E4"))
                      return;
                    break;
                  case 6:
                    if (!sbp.eq_s_b(1, "\u00F6"))
                      return;
                    break;
                  case 7:
                    v_2 = sbp.limit - sbp.cursor;
                    if (!r_LONG()) {
                      sbp.cursor = sbp.limit - v_2;
                      if (!sbp.eq_s_b(2, "ie")) {
                        sbp.cursor = sbp.limit - v_2;
                        break;
                      }
                    }
                    sbp.cursor = sbp.limit - v_2;
                    if (sbp.cursor <= sbp.limit_backward) {
                      sbp.cursor = sbp.limit - v_2;
                      break;
                    }
                    sbp.cursor--;
                    sbp.bra = sbp.cursor;
                    break;
                  case 8:
                    if (!sbp.in_grouping_b(g_V1, 97, 246) ||
                      !sbp.out_grouping_b(g_V1, 97, 246))
                      return;
                    break;
                }
                sbp.slice_del();
                B_ending_removed = true;
              } else
                sbp.limit_backward = v_1;
            }
          }

          function r_other_endings() {
            var among_var, v_1, v_2;
            if (sbp.cursor >= I_p2) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p2;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_7, 14);
              if (among_var) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_1;
                if (among_var == 1) {
                  v_2 = sbp.limit - sbp.cursor;
                  if (sbp.eq_s_b(2, "po"))
                    return;
                  sbp.cursor = sbp.limit - v_2;
                }
                sbp.slice_del();
              } else
                sbp.limit_backward = v_1;
            }
          }

          function r_i_plural() {
            var v_1;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              if (sbp.find_among_b(a_8, 2)) {
                sbp.bra = sbp.cursor;
                sbp.limit_backward = v_1;
                sbp.slice_del();
              } else
                sbp.limit_backward = v_1;
            }
          }

          function r_t_plural() {
            var among_var, v_1, v_2, v_3, v_4, v_5;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              sbp.ket = sbp.cursor;
              if (sbp.eq_s_b(1, "t")) {
                sbp.bra = sbp.cursor;
                v_2 = sbp.limit - sbp.cursor;
                if (sbp.in_grouping_b(g_V1, 97, 246)) {
                  sbp.cursor = sbp.limit - v_2;
                  sbp.slice_del();
                  sbp.limit_backward = v_1;
                  v_3 = sbp.limit - sbp.cursor;
                  if (sbp.cursor >= I_p2) {
                    sbp.cursor = I_p2;
                    v_4 = sbp.limit_backward;
                    sbp.limit_backward = sbp.cursor;
                    sbp.cursor = sbp.limit - v_3;
                    sbp.ket = sbp.cursor;
                    among_var = sbp.find_among_b(a_9, 2);
                    if (among_var) {
                      sbp.bra = sbp.cursor;
                      sbp.limit_backward = v_4;
                      if (among_var == 1) {
                        v_5 = sbp.limit - sbp.cursor;
                        if (sbp.eq_s_b(2, "po"))
                          return;
                        sbp.cursor = sbp.limit - v_5;
                      }
                      sbp.slice_del();
                      return;
                    }
                  }
                }
              }
              sbp.limit_backward = v_1;
            }
          }

          function r_tidy() {
            var v_1, v_2, v_3, v_4;
            if (sbp.cursor >= I_p1) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_p1;
              v_2 = sbp.limit - sbp.cursor;
              if (r_LONG()) {
                sbp.cursor = sbp.limit - v_2;
                sbp.ket = sbp.cursor;
                if (sbp.cursor > sbp.limit_backward) {
                  sbp.cursor--;
                  sbp.bra = sbp.cursor;
                  sbp.slice_del();
                }
              }
              sbp.cursor = sbp.limit - v_2;
              sbp.ket = sbp.cursor;
              if (sbp.in_grouping_b(g_AEI, 97, 228)) {
                sbp.bra = sbp.cursor;
                if (sbp.out_grouping_b(g_V1, 97, 246))
                  sbp.slice_del();
              }
              sbp.cursor = sbp.limit - v_2;
              sbp.ket = sbp.cursor;
              if (sbp.eq_s_b(1, "j")) {
                sbp.bra = sbp.cursor;
                v_3 = sbp.limit - sbp.cursor;
                if (!sbp.eq_s_b(1, "o")) {
                  sbp.cursor = sbp.limit - v_3;
                  if (sbp.eq_s_b(1, "u"))
                    sbp.slice_del();
                } else
                  sbp.slice_del();
              }
              sbp.cursor = sbp.limit - v_2;
              sbp.ket = sbp.cursor;
              if (sbp.eq_s_b(1, "o")) {
                sbp.bra = sbp.cursor;
                if (sbp.eq_s_b(1, "j"))
                  sbp.slice_del();
              }
              sbp.cursor = sbp.limit - v_2;
              sbp.limit_backward = v_1;
              while (true) {
                v_4 = sbp.limit - sbp.cursor;
                if (sbp.out_grouping_b(g_V1, 97, 246)) {
                  sbp.cursor = sbp.limit - v_4;
                  break;
                }
                sbp.cursor = sbp.limit - v_4;
                if (sbp.cursor <= sbp.limit_backward)
                  return;
                sbp.cursor--;
              }
              sbp.ket = sbp.cursor;
              if (sbp.cursor > sbp.limit_backward) {
                sbp.cursor--;
                sbp.bra = sbp.cursor;
                S_x = sbp.slice_to();
                if (sbp.eq_v_b(S_x))
                  sbp.slice_del();
              }
            }
          }
          this.stem = function() {
            var v_1 = sbp.cursor;
            r_mark_regions();
            B_ending_removed = false;
            sbp.limit_backward = v_1;
            sbp.cursor = sbp.limit;
            r_particle_etc();
            sbp.cursor = sbp.limit;
            r_possessive();
            sbp.cursor = sbp.limit;
            r_case_ending();
            sbp.cursor = sbp.limit;
            r_other_endings();
            sbp.cursor = sbp.limit;
            if (B_ending_removed) {
              r_i_plural();
              sbp.cursor = sbp.limit;
            } else {
              sbp.cursor = sbp.limit;
              r_t_plural();
              sbp.cursor = sbp.limit;
            }
            r_tidy();
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

    lunr.Pipeline.registerFunction(lunr.fi.stemmer, 'stemmer-fi');

    lunr.fi.stopWordFilter = lunr.generateStopWordFilter('ei eivät emme en et ette että he heidän heidät heihin heille heillä heiltä heissä heistä heitä hän häneen hänelle hänellä häneltä hänen hänessä hänestä hänet häntä itse ja johon joiden joihin joiksi joilla joille joilta joina joissa joista joita joka joksi jolla jolle jolta jona jonka jos jossa josta jota jotka kanssa keiden keihin keiksi keille keillä keiltä keinä keissä keistä keitä keneen keneksi kenelle kenellä keneltä kenen kenenä kenessä kenestä kenet ketkä ketkä ketä koska kuin kuka kun me meidän meidät meihin meille meillä meiltä meissä meistä meitä mihin miksi mikä mille millä miltä minkä minkä minua minulla minulle minulta minun minussa minusta minut minuun minä minä missä mistä mitkä mitä mukaan mutta ne niiden niihin niiksi niille niillä niiltä niin niin niinä niissä niistä niitä noiden noihin noiksi noilla noille noilta noin noina noissa noista noita nuo nyt näiden näihin näiksi näille näillä näiltä näinä näissä näistä näitä nämä ole olemme olen olet olette oli olimme olin olisi olisimme olisin olisit olisitte olisivat olit olitte olivat olla olleet ollut on ovat poikki se sekä sen siihen siinä siitä siksi sille sillä sillä siltä sinua sinulla sinulle sinulta sinun sinussa sinusta sinut sinuun sinä sinä sitä tai te teidän teidät teihin teille teillä teiltä teissä teistä teitä tuo tuohon tuoksi tuolla tuolle tuolta tuon tuona tuossa tuosta tuota tähän täksi tälle tällä tältä tämä tämän tänä tässä tästä tätä vaan vai vaikka yli'.split(' '));

    lunr.Pipeline.registerFunction(lunr.fi.stopWordFilter, 'stopWordFilter-fi');
  };
}))
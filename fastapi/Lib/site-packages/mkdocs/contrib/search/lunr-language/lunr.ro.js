/*!
 * Lunr languages, `Romanian` language
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
    lunr.ro = function() {
      this.pipeline.reset();
      this.pipeline.add(
        lunr.ro.trimmer,
        lunr.ro.stopWordFilter,
        lunr.ro.stemmer
      );

      // for lunr version 2
      // this is necessary so that every searched word is also stemmed before
      // in lunr <= 1 this is not needed, as it is done using the normal pipeline
      if (this.searchPipeline) {
        this.searchPipeline.reset();
        this.searchPipeline.add(lunr.ro.stemmer)
      }
    };

    /* lunr trimmer function */
    lunr.ro.wordCharacters = "A-Za-z\xAA\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u02E0-\u02E4\u1D00-\u1D25\u1D2C-\u1D5C\u1D62-\u1D65\u1D6B-\u1D77\u1D79-\u1DBE\u1E00-\u1EFF\u2071\u207F\u2090-\u209C\u212A\u212B\u2132\u214E\u2160-\u2188\u2C60-\u2C7F\uA722-\uA787\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA7FF\uAB30-\uAB5A\uAB5C-\uAB64\uFB00-\uFB06\uFF21-\uFF3A\uFF41-\uFF5A";
    lunr.ro.trimmer = lunr.trimmerSupport.generateTrimmer(lunr.ro.wordCharacters);

    lunr.Pipeline.registerFunction(lunr.ro.trimmer, 'trimmer-ro');

    /* lunr stemmer function */
    lunr.ro.stemmer = (function() {
      /* create the wrapped stemmer object */
      var Among = lunr.stemmerSupport.Among,
        SnowballProgram = lunr.stemmerSupport.SnowballProgram,
        st = new function RomanianStemmer() {
          var a_0 = [new Among("", -1, 3), new Among("I", 0, 1), new Among("U", 0, 2)],
            a_1 = [
              new Among("ea", -1, 3), new Among("a\u0163ia", -1, 7),
              new Among("aua", -1, 2), new Among("iua", -1, 4),
              new Among("a\u0163ie", -1, 7), new Among("ele", -1, 3),
              new Among("ile", -1, 5), new Among("iile", 6, 4),
              new Among("iei", -1, 4), new Among("atei", -1, 6),
              new Among("ii", -1, 4), new Among("ului", -1, 1),
              new Among("ul", -1, 1), new Among("elor", -1, 3),
              new Among("ilor", -1, 4), new Among("iilor", 14, 4)
            ],
            a_2 = [
              new Among("icala", -1, 4), new Among("iciva", -1, 4),
              new Among("ativa", -1, 5), new Among("itiva", -1, 6),
              new Among("icale", -1, 4), new Among("a\u0163iune", -1, 5),
              new Among("i\u0163iune", -1, 6), new Among("atoare", -1, 5),
              new Among("itoare", -1, 6), new Among("\u0103toare", -1, 5),
              new Among("icitate", -1, 4), new Among("abilitate", -1, 1),
              new Among("ibilitate", -1, 2), new Among("ivitate", -1, 3),
              new Among("icive", -1, 4), new Among("ative", -1, 5),
              new Among("itive", -1, 6), new Among("icali", -1, 4),
              new Among("atori", -1, 5), new Among("icatori", 18, 4),
              new Among("itori", -1, 6), new Among("\u0103tori", -1, 5),
              new Among("icitati", -1, 4), new Among("abilitati", -1, 1),
              new Among("ivitati", -1, 3), new Among("icivi", -1, 4),
              new Among("ativi", -1, 5), new Among("itivi", -1, 6),
              new Among("icit\u0103i", -1, 4), new Among("abilit\u0103i", -1, 1),
              new Among("ivit\u0103i", -1, 3),
              new Among("icit\u0103\u0163i", -1, 4),
              new Among("abilit\u0103\u0163i", -1, 1),
              new Among("ivit\u0103\u0163i", -1, 3), new Among("ical", -1, 4),
              new Among("ator", -1, 5), new Among("icator", 35, 4),
              new Among("itor", -1, 6), new Among("\u0103tor", -1, 5),
              new Among("iciv", -1, 4), new Among("ativ", -1, 5),
              new Among("itiv", -1, 6), new Among("ical\u0103", -1, 4),
              new Among("iciv\u0103", -1, 4), new Among("ativ\u0103", -1, 5),
              new Among("itiv\u0103", -1, 6)
            ],
            a_3 = [new Among("ica", -1, 1),
              new Among("abila", -1, 1), new Among("ibila", -1, 1),
              new Among("oasa", -1, 1), new Among("ata", -1, 1),
              new Among("ita", -1, 1), new Among("anta", -1, 1),
              new Among("ista", -1, 3), new Among("uta", -1, 1),
              new Among("iva", -1, 1), new Among("ic", -1, 1),
              new Among("ice", -1, 1), new Among("abile", -1, 1),
              new Among("ibile", -1, 1), new Among("isme", -1, 3),
              new Among("iune", -1, 2), new Among("oase", -1, 1),
              new Among("ate", -1, 1), new Among("itate", 17, 1),
              new Among("ite", -1, 1), new Among("ante", -1, 1),
              new Among("iste", -1, 3), new Among("ute", -1, 1),
              new Among("ive", -1, 1), new Among("ici", -1, 1),
              new Among("abili", -1, 1), new Among("ibili", -1, 1),
              new Among("iuni", -1, 2), new Among("atori", -1, 1),
              new Among("osi", -1, 1), new Among("ati", -1, 1),
              new Among("itati", 30, 1), new Among("iti", -1, 1),
              new Among("anti", -1, 1), new Among("isti", -1, 3),
              new Among("uti", -1, 1), new Among("i\u015Fti", -1, 3),
              new Among("ivi", -1, 1), new Among("it\u0103i", -1, 1),
              new Among("o\u015Fi", -1, 1), new Among("it\u0103\u0163i", -1, 1),
              new Among("abil", -1, 1), new Among("ibil", -1, 1),
              new Among("ism", -1, 3), new Among("ator", -1, 1),
              new Among("os", -1, 1), new Among("at", -1, 1),
              new Among("it", -1, 1), new Among("ant", -1, 1),
              new Among("ist", -1, 3), new Among("ut", -1, 1),
              new Among("iv", -1, 1), new Among("ic\u0103", -1, 1),
              new Among("abil\u0103", -1, 1), new Among("ibil\u0103", -1, 1),
              new Among("oas\u0103", -1, 1), new Among("at\u0103", -1, 1),
              new Among("it\u0103", -1, 1), new Among("ant\u0103", -1, 1),
              new Among("ist\u0103", -1, 3), new Among("ut\u0103", -1, 1),
              new Among("iv\u0103", -1, 1)
            ],
            a_4 = [new Among("ea", -1, 1),
              new Among("ia", -1, 1), new Among("esc", -1, 1),
              new Among("\u0103sc", -1, 1), new Among("ind", -1, 1),
              new Among("\u00E2nd", -1, 1), new Among("are", -1, 1),
              new Among("ere", -1, 1), new Among("ire", -1, 1),
              new Among("\u00E2re", -1, 1), new Among("se", -1, 2),
              new Among("ase", 10, 1), new Among("sese", 10, 2),
              new Among("ise", 10, 1), new Among("use", 10, 1),
              new Among("\u00E2se", 10, 1), new Among("e\u015Fte", -1, 1),
              new Among("\u0103\u015Fte", -1, 1), new Among("eze", -1, 1),
              new Among("ai", -1, 1), new Among("eai", 19, 1),
              new Among("iai", 19, 1), new Among("sei", -1, 2),
              new Among("e\u015Fti", -1, 1), new Among("\u0103\u015Fti", -1, 1),
              new Among("ui", -1, 1), new Among("ezi", -1, 1),
              new Among("\u00E2i", -1, 1), new Among("a\u015Fi", -1, 1),
              new Among("se\u015Fi", -1, 2), new Among("ase\u015Fi", 29, 1),
              new Among("sese\u015Fi", 29, 2), new Among("ise\u015Fi", 29, 1),
              new Among("use\u015Fi", 29, 1),
              new Among("\u00E2se\u015Fi", 29, 1), new Among("i\u015Fi", -1, 1),
              new Among("u\u015Fi", -1, 1), new Among("\u00E2\u015Fi", -1, 1),
              new Among("a\u0163i", -1, 2), new Among("ea\u0163i", 38, 1),
              new Among("ia\u0163i", 38, 1), new Among("e\u0163i", -1, 2),
              new Among("i\u0163i", -1, 2), new Among("\u00E2\u0163i", -1, 2),
              new Among("ar\u0103\u0163i", -1, 1),
              new Among("ser\u0103\u0163i", -1, 2),
              new Among("aser\u0103\u0163i", 45, 1),
              new Among("seser\u0103\u0163i", 45, 2),
              new Among("iser\u0103\u0163i", 45, 1),
              new Among("user\u0103\u0163i", 45, 1),
              new Among("\u00E2ser\u0103\u0163i", 45, 1),
              new Among("ir\u0103\u0163i", -1, 1),
              new Among("ur\u0103\u0163i", -1, 1),
              new Among("\u00E2r\u0103\u0163i", -1, 1), new Among("am", -1, 1),
              new Among("eam", 54, 1), new Among("iam", 54, 1),
              new Among("em", -1, 2), new Among("asem", 57, 1),
              new Among("sesem", 57, 2), new Among("isem", 57, 1),
              new Among("usem", 57, 1), new Among("\u00E2sem", 57, 1),
              new Among("im", -1, 2), new Among("\u00E2m", -1, 2),
              new Among("\u0103m", -1, 2), new Among("ar\u0103m", 65, 1),
              new Among("ser\u0103m", 65, 2), new Among("aser\u0103m", 67, 1),
              new Among("seser\u0103m", 67, 2), new Among("iser\u0103m", 67, 1),
              new Among("user\u0103m", 67, 1),
              new Among("\u00E2ser\u0103m", 67, 1),
              new Among("ir\u0103m", 65, 1), new Among("ur\u0103m", 65, 1),
              new Among("\u00E2r\u0103m", 65, 1), new Among("au", -1, 1),
              new Among("eau", 76, 1), new Among("iau", 76, 1),
              new Among("indu", -1, 1), new Among("\u00E2ndu", -1, 1),
              new Among("ez", -1, 1), new Among("easc\u0103", -1, 1),
              new Among("ar\u0103", -1, 1), new Among("ser\u0103", -1, 2),
              new Among("aser\u0103", 84, 1), new Among("seser\u0103", 84, 2),
              new Among("iser\u0103", 84, 1), new Among("user\u0103", 84, 1),
              new Among("\u00E2ser\u0103", 84, 1), new Among("ir\u0103", -1, 1),
              new Among("ur\u0103", -1, 1), new Among("\u00E2r\u0103", -1, 1),
              new Among("eaz\u0103", -1, 1)
            ],
            a_5 = [new Among("a", -1, 1),
              new Among("e", -1, 1), new Among("ie", 1, 1),
              new Among("i", -1, 1), new Among("\u0103", -1, 1)
            ],
            g_v = [17, 65,
              16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 32, 0, 0, 4
            ],
            B_standard_suffix_removed, I_p2, I_p1, I_pV, sbp = new SnowballProgram();
          this.setCurrent = function(word) {
            sbp.setCurrent(word);
          };
          this.getCurrent = function() {
            return sbp.getCurrent();
          };

          function habr1(c1, c2) {
            if (sbp.eq_s(1, c1)) {
              sbp.ket = sbp.cursor;
              if (sbp.in_grouping(g_v, 97, 259))
                sbp.slice_from(c2);
            }
          }

          function r_prelude() {
            var v_1, v_2;
            while (true) {
              v_1 = sbp.cursor;
              if (sbp.in_grouping(g_v, 97, 259)) {
                v_2 = sbp.cursor;
                sbp.bra = v_2;
                habr1("u", "U");
                sbp.cursor = v_2;
                habr1("i", "I");
              }
              sbp.cursor = v_1;
              if (sbp.cursor >= sbp.limit) {
                break;
              }
              sbp.cursor++;
            }
          }

          function habr2() {
            if (sbp.out_grouping(g_v, 97, 259)) {
              while (!sbp.in_grouping(g_v, 97, 259)) {
                if (sbp.cursor >= sbp.limit)
                  return true;
                sbp.cursor++;
              }
              return false;
            }
            return true;
          }

          function habr3() {
            if (sbp.in_grouping(g_v, 97, 259)) {
              while (!sbp.out_grouping(g_v, 97, 259)) {
                if (sbp.cursor >= sbp.limit)
                  return true;
                sbp.cursor++;
              }
            }
            return false;
          }

          function habr4() {
            var v_1 = sbp.cursor,
              v_2, v_3;
            if (sbp.in_grouping(g_v, 97, 259)) {
              v_2 = sbp.cursor;
              if (habr2()) {
                sbp.cursor = v_2;
                if (!habr3()) {
                  I_pV = sbp.cursor;
                  return;
                }
              } else {
                I_pV = sbp.cursor;
                return;
              }
            }
            sbp.cursor = v_1;
            if (sbp.out_grouping(g_v, 97, 259)) {
              v_3 = sbp.cursor;
              if (habr2()) {
                sbp.cursor = v_3;
                if (sbp.in_grouping(g_v, 97, 259) && sbp.cursor < sbp.limit)
                  sbp.cursor++;
              }
              I_pV = sbp.cursor;
            }
          }

          function habr5() {
            while (!sbp.in_grouping(g_v, 97, 259)) {
              if (sbp.cursor >= sbp.limit)
                return false;
              sbp.cursor++;
            }
            while (!sbp.out_grouping(g_v, 97, 259)) {
              if (sbp.cursor >= sbp.limit)
                return false;
              sbp.cursor++;
            }
            return true;
          }

          function r_mark_regions() {
            var v_1 = sbp.cursor;
            I_pV = sbp.limit;
            I_p1 = I_pV;
            I_p2 = I_pV;
            habr4();
            sbp.cursor = v_1;
            if (habr5()) {
              I_p1 = sbp.cursor;
              if (habr5())
                I_p2 = sbp.cursor;
            }
          }

          function r_postlude() {
            var among_var;
            while (true) {
              sbp.bra = sbp.cursor;
              among_var = sbp.find_among(a_0, 3);
              if (among_var) {
                sbp.ket = sbp.cursor;
                switch (among_var) {
                  case 1:
                    sbp.slice_from("i");
                    continue;
                  case 2:
                    sbp.slice_from("u");
                    continue;
                  case 3:
                    if (sbp.cursor >= sbp.limit)
                      break;
                    sbp.cursor++;
                    continue;
                }
              }
              break;
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

          function r_step_0() {
            var among_var, v_1;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_1, 16);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    break;
                  case 2:
                    sbp.slice_from("a");
                    break;
                  case 3:
                    sbp.slice_from("e");
                    break;
                  case 4:
                    sbp.slice_from("i");
                    break;
                  case 5:
                    v_1 = sbp.limit - sbp.cursor;
                    if (!sbp.eq_s_b(2, "ab")) {
                      sbp.cursor = sbp.limit - v_1;
                      sbp.slice_from("i");
                    }
                    break;
                  case 6:
                    sbp.slice_from("at");
                    break;
                  case 7:
                    sbp.slice_from("a\u0163i");
                    break;
                }
              }
            }
          }

          function r_combo_suffix() {
            var among_var, v_1 = sbp.limit - sbp.cursor;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_2, 46);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R1()) {
                switch (among_var) {
                  case 1:
                    sbp.slice_from("abil");
                    break;
                  case 2:
                    sbp.slice_from("ibil");
                    break;
                  case 3:
                    sbp.slice_from("iv");
                    break;
                  case 4:
                    sbp.slice_from("ic");
                    break;
                  case 5:
                    sbp.slice_from("at");
                    break;
                  case 6:
                    sbp.slice_from("it");
                    break;
                }
                B_standard_suffix_removed = true;
                sbp.cursor = sbp.limit - v_1;
                return true;
              }
            }
            return false;
          }

          function r_standard_suffix() {
            var among_var, v_1;
            B_standard_suffix_removed = false;
            while (true) {
              v_1 = sbp.limit - sbp.cursor;
              if (!r_combo_suffix()) {
                sbp.cursor = sbp.limit - v_1;
                break;
              }
            }
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_3, 62);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_R2()) {
                switch (among_var) {
                  case 1:
                    sbp.slice_del();
                    break;
                  case 2:
                    if (sbp.eq_s_b(1, "\u0163")) {
                      sbp.bra = sbp.cursor;
                      sbp.slice_from("t");
                    }
                    break;
                  case 3:
                    sbp.slice_from("ist");
                    break;
                }
                B_standard_suffix_removed = true;
              }
            }
          }

          function r_verb_suffix() {
            var among_var, v_1, v_2;
            if (sbp.cursor >= I_pV) {
              v_1 = sbp.limit_backward;
              sbp.limit_backward = I_pV;
              sbp.ket = sbp.cursor;
              among_var = sbp.find_among_b(a_4, 94);
              if (among_var) {
                sbp.bra = sbp.cursor;
                switch (among_var) {
                  case 1:
                    v_2 = sbp.limit - sbp.cursor;
                    if (!sbp.out_grouping_b(g_v, 97, 259)) {
                      sbp.cursor = sbp.limit - v_2;
                      if (!sbp.eq_s_b(1, "u"))
                        break;
                    }
                  case 2:
                    sbp.slice_del();
                    break;
                }
              }
              sbp.limit_backward = v_1;
            }
          }

          function r_vowel_suffix() {
            var among_var;
            sbp.ket = sbp.cursor;
            among_var = sbp.find_among_b(a_5, 5);
            if (among_var) {
              sbp.bra = sbp.cursor;
              if (r_RV() && among_var == 1)
                sbp.slice_del();
            }
          }
          this.stem = function() {
            var v_1 = sbp.cursor;
            r_prelude();
            sbp.cursor = v_1;
            r_mark_regions();
            sbp.limit_backward = v_1;
            sbp.cursor = sbp.limit;
            r_step_0();
            sbp.cursor = sbp.limit;
            r_standard_suffix();
            sbp.cursor = sbp.limit;
            if (!B_standard_suffix_removed) {
              sbp.cursor = sbp.limit;
              r_verb_suffix();
              sbp.cursor = sbp.limit;
            }
            r_vowel_suffix();
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

    lunr.Pipeline.registerFunction(lunr.ro.stemmer, 'stemmer-ro');

    lunr.ro.stopWordFilter = lunr.generateStopWordFilter('acea aceasta această aceea acei aceia acel acela acele acelea acest acesta aceste acestea aceşti aceştia acolo acord acum ai aia aibă aici al ale alea altceva altcineva am ar are asemenea asta astea astăzi asupra au avea avem aveţi azi aş aşadar aţi bine bucur bună ca care caut ce cel ceva chiar cinci cine cineva contra cu cum cumva curând curînd când cât câte câtva câţi cînd cît cîte cîtva cîţi că căci cărei căror cărui către da dacă dar datorită dată dau de deci deja deoarece departe deşi din dinaintea dintr- dintre doi doilea două drept după dă ea ei el ele eram este eu eşti face fata fi fie fiecare fii fim fiu fiţi frumos fără graţie halbă iar ieri la le li lor lui lângă lîngă mai mea mei mele mereu meu mi mie mine mult multă mulţi mulţumesc mâine mîine mă ne nevoie nici nicăieri nimeni nimeri nimic nişte noastre noastră noi noroc nostru nouă noştri nu opt ori oricare orice oricine oricum oricând oricât oricînd oricît oriunde patra patru patrulea pe pentru peste pic poate pot prea prima primul prin puţin puţina puţină până pînă rog sa sale sau se spate spre sub sunt suntem sunteţi sută sînt sîntem sînteţi să săi său ta tale te timp tine toate toată tot totuşi toţi trei treia treilea tu tăi tău un una unde undeva unei uneia unele uneori unii unor unora unu unui unuia unul vi voastre voastră voi vostru vouă voştri vreme vreo vreun vă zece zero zi zice îi îl îmi împotriva în  înainte înaintea încotro încât încît între întrucât întrucît îţi ăla ălea ăsta ăstea ăştia şapte şase şi ştiu ţi ţie'.split(' '));

    lunr.Pipeline.registerFunction(lunr.ro.stopWordFilter, 'stopWordFilter-ro');
  };
}))
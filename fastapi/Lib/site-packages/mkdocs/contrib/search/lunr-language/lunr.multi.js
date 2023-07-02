/**
 * export the module via AMD, CommonJS or as a browser global
 * Export code from https://github.com/umdjs/umd/blob/master/returnExports.js
 */
;(function (root, factory) {
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
}(this, function () {
    /**
     * Just return a value to define the module export.
     * This example returns an object, but the module
     * can return a function as the exported value.
     */
    return function(lunr) {
        /* Set up the pipeline for indexing content in multiple languages. The
           corresponding lunr.{lang} files must be loaded before calling this
           function; English ('en') is built in.

           Returns: a lunr plugin for use in your indexer.

           Known drawback: every word will be stemmed with stemmers for every
           language. This could mean that sometimes words that have the same
           stemming root will not be stemmed as such.
           */
        lunr.multiLanguage = function(/* lang1, lang2, ... */) {
            var languages = Array.prototype.slice.call(arguments);
            var nameSuffix = languages.join('-');
            var wordCharacters = "";
            var pipeline = [];
            var searchPipeline = [];
            for (var i = 0; i < languages.length; ++i) {
                if (languages[i] == 'en') {
                    wordCharacters += '\\w';
                    pipeline.unshift(lunr.stopWordFilter);
                    pipeline.push(lunr.stemmer);
                    searchPipeline.push(lunr.stemmer);
                } else {
                    wordCharacters += lunr[languages[i]].wordCharacters;
                    if (lunr[languages[i]].stopWordFilter) {
                        pipeline.unshift(lunr[languages[i]].stopWordFilter);
                    }
                    if (lunr[languages[i]].stemmer) {
                        pipeline.push(lunr[languages[i]].stemmer);
                        searchPipeline.push(lunr[languages[i]].stemmer);
                    }
                }
            };
            var multiTrimmer = lunr.trimmerSupport.generateTrimmer(wordCharacters);
            lunr.Pipeline.registerFunction(multiTrimmer, 'lunr-multi-trimmer-' + nameSuffix);
            pipeline.unshift(multiTrimmer);

            return function() {
                this.pipeline.reset();

                this.pipeline.add.apply(this.pipeline, pipeline);

                // for lunr version 2
                // this is necessary so that every searched word is also stemmed before
                // in lunr <= 1 this is not needed, as it is done using the normal pipeline
                if (this.searchPipeline) {
                    this.searchPipeline.reset();
                    this.searchPipeline.add.apply(this.searchPipeline, searchPipeline);
                }
            };
        }
    }
}));

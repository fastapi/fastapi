/**
 * termynal.js
 * A lightweight, modern and extensible animated terminal window, using
 * async/await.
 *
 * @author Ines Montani <ines@ines.io>
 * @version 0.0.1
 * @license MIT
 */

'use strict';

/** Generate a terminal widget. */
class Termynal {
    /**
     * Construct the widget's settings.
     * @param {(string|Node)=} container - Query selector or container element.
     * @param {Object=} options - Custom settings.
     * @param {string} options.prefix - Prefix to use for data attributes.
     * @param {number} options.startDelay - Delay before animation, in ms.
     * @param {number} options.typeDelay - Delay between each typed character, in ms.
     * @param {number} options.lineDelay - Delay between each line, in ms.
     * @param {number} options.progressLength - Number of characters displayed as progress bar.
     * @param {string} options.progressChar – Character to use for progress bar, defaults to █.
	 * @param {number} options.progressPercent - Max percent of progress.
     * @param {string} options.cursor – Character to use for cursor, defaults to ▋.
     * @param {Object[]} lineData - Dynamically loaded line data objects.
     * @param {boolean} options.noInit - Don't initialise the animation.
     */
    constructor(container = '#termynal', options = {}) {
        this.container = (typeof container === 'string') ? document.querySelector(container) : container;
        this.pfx = `data-${options.prefix || 'ty'}`;
        this.originalStartDelay = this.startDelay = options.startDelay
            || parseFloat(this.container.getAttribute(`${this.pfx}-startDelay`)) || 600;
        this.originalTypeDelay = this.typeDelay = options.typeDelay
            || parseFloat(this.container.getAttribute(`${this.pfx}-typeDelay`)) || 90;
        this.originalLineDelay = this.lineDelay = options.lineDelay
            || parseFloat(this.container.getAttribute(`${this.pfx}-lineDelay`)) || 1500;
        this.progressLength = options.progressLength
            || parseFloat(this.container.getAttribute(`${this.pfx}-progressLength`)) || 40;
        this.progressChar = options.progressChar
            || this.container.getAttribute(`${this.pfx}-progressChar`) || '█';
		this.progressPercent = options.progressPercent
            || parseFloat(this.container.getAttribute(`${this.pfx}-progressPercent`)) || 100;
        this.cursor = options.cursor
            || this.container.getAttribute(`${this.pfx}-cursor`) || '▋';
        this.lineData = this.lineDataToElements(options.lineData || []);
        this.loadLines()
        if (!options.noInit) this.init()
    }

    loadLines() {
        // Load all the lines and create the container so that the size is fixed
        // Otherwise it would be changing and the user viewport would be constantly
        // moving as she/he scrolls
        const finish = this.generateFinish()
        finish.style.visibility = 'hidden'
        this.container.appendChild(finish)
        // Appends dynamically loaded lines to existing line elements.
        this.lines = [...this.container.querySelectorAll(`[${this.pfx}]`)].concat(this.lineData);
        for (let line of this.lines) {
            line.style.visibility = 'hidden'
            this.container.appendChild(line)
        }
        const restart = this.generateRestart()
        restart.style.visibility = 'hidden'
        this.container.appendChild(restart)
        this.container.setAttribute('data-termynal', '');
    }

    /**
     * Initialise the widget, get lines, clear container and start animation.
     */
    init() {
        /** 
         * Calculates width and height of Termynal container.
         * If container is empty and lines are dynamically loaded, defaults to browser `auto` or CSS.
         */ 
        const containerStyle = getComputedStyle(this.container);
        this.container.style.width = containerStyle.width !== '0px' ? 
            containerStyle.width : undefined;
        this.container.style.minHeight = containerStyle.height !== '0px' ? 
            containerStyle.height : undefined;

        this.container.setAttribute('data-termynal', '');
        this.container.innerHTML = '';
        for (let line of this.lines) {
            line.style.visibility = 'visible'
        }
        this.start();
    }

    /**
     * Start the animation and rener the lines depending on their data attributes.
     */
    async start() {
        this.addFinish()
        await this._wait(this.startDelay);

        for (let line of this.lines) {
            const type = line.getAttribute(this.pfx);
            const delay = line.getAttribute(`${this.pfx}-delay`) || this.lineDelay;

            if (type == 'input') {
                line.setAttribute(`${this.pfx}-cursor`, this.cursor);
                await this.type(line);
                await this._wait(delay);
            }

            else if (type == 'progress') {
                await this.progress(line);
                await this._wait(delay);
            }

            else {
                this.container.appendChild(line);
                await this._wait(delay);
            }

            line.removeAttribute(`${this.pfx}-cursor`);
        }
        this.addRestart()
        this.finishElement.style.visibility = 'hidden'
        this.lineDelay = this.originalLineDelay
        this.typeDelay = this.originalTypeDelay
        this.startDelay = this.originalStartDelay
    }

    generateRestart() {
        const restart = document.createElement('a')
        restart.onclick = (e) => {
            e.preventDefault()
            this.container.innerHTML = ''
            this.init()
        }
        restart.href = '#'
        restart.setAttribute('data-terminal-control', '')
        restart.innerHTML = "restart ↻"
        return restart
    }
    
    generateFinish() {
        const finish = document.createElement('a')
        finish.onclick = (e) => {
            e.preventDefault()
            this.lineDelay = 0
            this.typeDelay = 0
            this.startDelay = 0
        }
        finish.href = '#'
        finish.setAttribute('data-terminal-control', '')
        finish.innerHTML = "fast →"
        this.finishElement = finish
        return finish
    }

    addRestart() {
        const restart = this.generateRestart()
        this.container.appendChild(restart)
    }

    addFinish() {
        const finish = this.generateFinish()
        this.container.appendChild(finish)
    }

    /**
     * Animate a typed line.
     * @param {Node} line - The line element to render.
     */
    async type(line) {
        const chars = [...line.textContent];
        line.textContent = '';
        this.container.appendChild(line);

        for (let char of chars) {
            const delay = line.getAttribute(`${this.pfx}-typeDelay`) || this.typeDelay;
            await this._wait(delay);
            line.textContent += char;
        }
    }

    /**
     * Animate a progress bar.
     * @param {Node} line - The line element to render.
     */
    async progress(line) {
        const progressLength = line.getAttribute(`${this.pfx}-progressLength`)
            || this.progressLength;
        const progressChar = line.getAttribute(`${this.pfx}-progressChar`)
            || this.progressChar;
        const chars = progressChar.repeat(progressLength);
		const progressPercent = line.getAttribute(`${this.pfx}-progressPercent`)
			|| this.progressPercent;
        line.textContent = '';
        this.container.appendChild(line);

        for (let i = 1; i < chars.length + 1; i++) {
            await this._wait(this.typeDelay);
            const percent = Math.round(i / chars.length * 100);
            line.textContent = `${chars.slice(0, i)} ${percent}%`;
			if (percent>progressPercent) {
				break;
			}
        }
    }

    /**
     * Helper function for animation delays, called with `await`.
     * @param {number} time - Timeout, in ms.
     */
    _wait(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }

    /**
     * Converts line data objects into line elements.
     * 
     * @param {Object[]} lineData - Dynamically loaded lines.
     * @param {Object} line - Line data object.
     * @returns {Element[]} - Array of line elements.
     */
    lineDataToElements(lineData) {
        return lineData.map(line => {
            let div = document.createElement('div');
            div.innerHTML = `<span ${this._attributes(line)}>${line.value || ''}</span>`;

            return div.firstElementChild;
        });
    }

    /**
     * Helper function for generating attributes string.
     * 
     * @param {Object} line - Line data object.
     * @returns {string} - String of attributes.
     */
    _attributes(line) {
        let attrs = '';
        for (let prop in line) {
            // Custom add class
            if (prop === 'class') {
                attrs += ` class=${line[prop]} `
                continue
            }
            if (prop === 'type') {
                attrs += `${this.pfx}="${line[prop]}" `
            } else if (prop !== 'value') {
                attrs += `${this.pfx}-${prop}="${line[prop]}" `
            }
        }

        return attrs;
    }
}

/**
* HTML API: If current script has container(s) specified, initialise Termynal.
*/
if (document.currentScript.hasAttribute('data-termynal-container')) {
    const containers = document.currentScript.getAttribute('data-termynal-container');
    containers.split('|')
        .forEach(container => new Termynal(container))
}

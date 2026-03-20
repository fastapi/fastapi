function setupTermynal() {
    document.querySelectorAll(".use-termynal").forEach(node => {
        node.style.display = "block";
        new Termynal(node, {
            lineDelay: 500
        });
    });
    const progressLiteralStart = "---> 100%";
    const promptLiteralStart = "$ ";
    const customPromptLiteralStart = "# ";
    const termynalActivateClass = "termy";
    let termynals = [];

    function createTermynals() {
        document
            .querySelectorAll(`.${termynalActivateClass} .highlight code`)
            .forEach(node => {
                const text = node.textContent;
                const lines = text.split("\n");
                const useLines = [];
                let buffer = [];
                function saveBuffer() {
                    if (buffer.length) {
                        let isBlankSpace = true;
                        buffer.forEach(line => {
                            if (line) {
                                isBlankSpace = false;
                            }
                        });
                        dataValue = {};
                        if (isBlankSpace) {
                            dataValue["delay"] = 0;
                        }
                        if (buffer[buffer.length - 1] === "") {
                            // A last single <br> won't have effect
                            // so put an additional one
                            buffer.push("");
                        }
                        const bufferValue = buffer.join("<br>");
                        dataValue["value"] = bufferValue;
                        useLines.push(dataValue);
                        buffer = [];
                    }
                }
                for (let line of lines) {
                    if (line === progressLiteralStart) {
                        saveBuffer();
                        useLines.push({
                            type: "progress"
                        });
                    } else if (line.startsWith(promptLiteralStart)) {
                        saveBuffer();
                        const value = line.replace(promptLiteralStart, "").trimEnd();
                        useLines.push({
                            type: "input",
                            value: value
                        });
                    } else if (line.startsWith("// ")) {
                        saveBuffer();
                        const value = "💬 " + line.replace("// ", "").trimEnd();
                        useLines.push({
                            value: value,
                            class: "termynal-comment",
                            delay: 0
                        });
                    } else if (line.startsWith(customPromptLiteralStart)) {
                        saveBuffer();
                        const promptStart = line.indexOf(promptLiteralStart);
                        if (promptStart === -1) {
                            console.error("Custom prompt found but no end delimiter", line)
                        }
                        const prompt = line.slice(0, promptStart).replace(customPromptLiteralStart, "")
                        let value = line.slice(promptStart + promptLiteralStart.length);
                        useLines.push({
                            type: "input",
                            value: value,
                            prompt: prompt
                        });
                    } else {
                        buffer.push(line);
                    }
                }
                saveBuffer();
                const inputCommands = useLines
                    .filter(line => line.type === "input")
                    .map(line => line.value)
                    .join("\n");
                node.textContent = inputCommands;
                const div = document.createElement("div");
                node.style.display = "none";
                node.after(div);
                const termynal = new Termynal(div, {
                    lineData: useLines,
                    noInit: true,
                    lineDelay: 500
                });
                termynals.push(termynal);
            });
    }

    function loadVisibleTermynals() {
        termynals = termynals.filter(termynal => {
            if (termynal.container.getBoundingClientRect().top - innerHeight <= 0) {
                termynal.init();
                return false;
            }
            return true;
        });
    }
    window.addEventListener("scroll", loadVisibleTermynals);
    createTermynals();
    loadVisibleTermynals();
}

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
    while (0 !== currentIndex) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
    return array;
}

async function showRandomAnnouncement(groupId, timeInterval) {
    const announceFastAPI = document.getElementById(groupId);
    if (announceFastAPI) {
        let children = [].slice.call(announceFastAPI.children);
        children = shuffle(children)
        let index = 0
        const announceRandom = () => {
            children.forEach((el, i) => { el.style.display = "none" });
            children[index].style.display = "block"
            index = (index + 1) % children.length
        }
        announceRandom()
        setInterval(announceRandom, timeInterval
        )
    }
}

function handleSponsorImages() {
    const announceRight = document.getElementById('announce-right');
    if(!announceRight) return;

    const sponsorImages = document.querySelectorAll('.sponsor-image');

    const imagePromises = Array.from(sponsorImages).map(img => {
        return new Promise((resolve, reject) => {
            if (img.complete && img.naturalHeight !== 0) {
                resolve();
            } else {
                img.addEventListener('load', () => {
                    if (img.naturalHeight !== 0) {
                        resolve();
                    } else {
                        reject();
                    }
                });
                img.addEventListener('error', reject);
            }
        });
    });

    Promise.all(imagePromises)
        .then(() => {
            announceRight.style.display = 'block';
            showRandomAnnouncement('announce-right', 10000);
        })
        .catch(() => {
            // do nothing
        });
}

function openLinksInNewTab() {
    const siteUrl = document.querySelector("link[rel='canonical']")?.href
        || window.location.origin;
    const siteOrigin = new URL(siteUrl).origin;
    document.querySelectorAll(".md-content a[href]").forEach(a => {
        if (a.getAttribute("target") === "_self") return;
        const href = a.getAttribute("href");
        if (!href) return;
        try {
            const url = new URL(href, window.location.href);
            // Skip same-page anchor links (only the hash differs)
            if (url.origin === window.location.origin
                && url.pathname === window.location.pathname
                && url.search === window.location.search) return;
            if (!a.hasAttribute("target")) {
                a.setAttribute("target", "_blank");
                a.setAttribute("rel", "noopener");
            }
            if (url.origin !== siteOrigin) {
                a.dataset.externalLink = "";
            } else {
                a.dataset.internalLink = "";
            }
        } catch (_) {}
    });
}

async function main() {
    setupTermynal();
    showRandomAnnouncement('announce-left', 5000)
    handleSponsorImages();
    openLinksInNewTab();
}
document$.subscribe(() => {
    main()
})

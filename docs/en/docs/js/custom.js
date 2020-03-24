const div = document.querySelector('.github-topic-projects')

async function getDataBatch(page) {
    const response = await fetch(`https://api.github.com/search/repositories?q=topic:fastapi&per_page=100&page=${page}`, { headers: { Accept: 'application/vnd.github.mercy-preview+json' } })
    const data = await response.json()
    return data
}

async function getData() {
    let page = 1
    let data = []
    let dataBatch = await getDataBatch(page)
    data = data.concat(dataBatch.items)
    const totalCount = dataBatch.total_count
    while (data.length < totalCount) {
        page += 1
        dataBatch = await getDataBatch(page)
        data = data.concat(dataBatch.items)
    }
    return data
}

async function main() {
    if (div) {
        data = await getData()
        div.innerHTML = '<ul></ul>'
        const ul = document.querySelector('.github-topic-projects ul')
        data.forEach(v => {
            if (v.full_name === 'tiangolo/fastapi') {
                return
            }
            const li = document.createElement('li')
            li.innerHTML = `<a href="${v.html_url}" target="_blank">★ ${v.stargazers_count} - ${v.full_name}</a> by <a href="${v.owner.html_url}" target="_blank">@${v.owner.login}</a>`
            ul.append(li)
        })
    }
}

main()

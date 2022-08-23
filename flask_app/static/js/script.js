const quote = document.querySelector('#quote');
const quoteAuthor = document.querySelector('#quote-author');
const generateNewQuote = document.querySelector('#generate-new-quote');

const url = 'https://api.quotable.io/random?tags=inspirational';

function getQuote() {
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        quote.innerText = data.content;
        quoteAuthor.innerText = data.author;
    })
        .catch(err => console.log(err))
}

window.addEventListener('load', getQuote);
// generateNewQuote.addEventListener('click', getQuote);
let count = 0;
let uniques = new Set();

$('.user-word').on('submit',async function (e) {
    e.preventDefault();

    const $msg = $('.msg');
    const $score = $('.score');
    const $word = $('#word');
    const form = $('.user-word');
    let highscore = $('#highscore');
    let userword = $('.word-container');
    let word = $word.val();
    let btn = $('.submit');

    if(word === "") {
        return;
    }

    count++;

    const response = await axios.get('/check-word',{
        params: {word: word},
    });
    $msg.text('');
    $word.val('');

    if(response.data.result === 'not-word') {
        $msg.append(`${word} is not a valid word!`);
    } else if(response.data.result === 'not-on-board') {
        $msg.append(`${word} is not listed on the board.`)
    } else {
        let val = parseInt($score.text());

        if(uniques.has(word)) {
            $msg.append(`${word} already found!`);
        } else {
            $score.text((val += word.length));
            userword.append(`<li> ${word} </li>`);
            uniques.add(word);
            $msg.append(`${word} added!`);
        }
    }

    let timer = 20;
    if(count === 1) {
        let interval = setInterval(async function () {
            timer--;
            if(timer === 0) {
                clearInterval(interval);
                $('#timer').html('<h2> Game Over! </h2>');
                btn.disabled = true;
                $msg.hide();

                const response = await axios.post('/user-score',{
                    $score: parseInt($score.text()),
                });

                if(response.data.brokeRecord) {
                    highscore.append(`New record: ${score}`)
                }
                return;
            } else {
                $('#time').text(timer);
            }
        },1000);
    }
})
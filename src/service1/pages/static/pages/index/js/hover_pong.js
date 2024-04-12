document.addEventListener("DOMContentLoaded", function() {
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');

<<<<<<< HEAD

    if (indexSudoku && indexPong)
    {
        indexPong.addEventListener('mouseenter', function() {
            indexPong.classList.add('scaled-pong');
            indexSudoku.classList.add('shrunken-pong');
        });
    
        indexPong.addEventListener('mouseleave', function() {
            indexPong.classList.remove('scaled-pong');
            indexSudoku.classList.remove('shrunken-pong');
        });
    }
=======
    indexPong.addEventListener('mouseenter', function() {
        indexPong.classList.add('scaled-pong');
        indexSudoku.classList.add('shrunken-pong');
    });

    indexPong.addEventListener('mouseleave', function() {
        indexPong.classList.remove('scaled-pong');
        indexSudoku.classList.remove('shrunken-pong');
    });
>>>>>>> 248fe0e (🐛 fix: new architecture fixed)
});
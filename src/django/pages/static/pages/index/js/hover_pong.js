document.addEventListener("DOMContentLoaded", function() {
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');

    indexPong.addEventListener('mouseenter', function() {
        indexPong.classList.add('scaled-pong');
        indexSudoku.classList.add('shrunken-pong');
    });

    indexPong.addEventListener('mouseleave', function() {
        indexPong.classList.remove('scaled-pong');
        indexSudoku.classList.remove('shrunken-pong');
    });
});
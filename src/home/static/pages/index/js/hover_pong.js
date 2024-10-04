document.addEventListener("mouseover", function() {
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');


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
});
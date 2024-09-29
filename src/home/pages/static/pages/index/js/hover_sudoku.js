// // script.js
document.addEventListener("DOMContentLoaded", function() {
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');
    
    indexSudoku.addEventListener('mouseenter', function() {
        indexSudoku.classList.add('scaled-sudoku');
        indexPong.classList.add('shrunken-sudoku');
    });
    
    indexSudoku.addEventListener('mouseleave', function() {
        indexSudoku.classList.remove('scaled-sudoku');
        indexPong.classList.remove('shrunken-sudoku');
    });
});
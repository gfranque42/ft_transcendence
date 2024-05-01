// // script.js
document.addEventListener("DOMContentLoaded", function() {
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');
    

    // if (indexSudoku && indexPong)
    // {
        indexSudoku.addEventListener('mouseenter', function() {
            indexSudoku.classList.add('scaled-sudoku');
            indexPong.classList.add('shrunken-sudoku');
        });
        
        indexSudoku.addEventListener('mouseleave', function() {
            indexSudoku.classList.remove('scaled-sudoku');
            indexPong.classList.remove('shrunken-sudoku');
        });
    // }
});

document.addEventListener("DOMContentLoaded", function() {
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');


    // if (indexSudoku && indexPong)
    // {
        indexPong.addEventListener('mouseenter', function() {
            indexPong.classList.add('scaled-pong');
            indexSudoku.classList.add('shrunken-pong');
        });
    
        indexPong.addEventListener('mouseleave', function() {
            indexPong.classList.remove('scaled-pong');
            indexSudoku.classList.remove('shrunken-pong');
        });
    // }
});
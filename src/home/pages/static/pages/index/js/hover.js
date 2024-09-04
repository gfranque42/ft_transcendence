// document.addEventListener("DOMContentLoaded", function() {
//     const indexPong = document.querySelector('.index-pong');
//     const indexSudoku = document.querySelector('.index-sudoku');
    
//     if (indexSudoku && indexPong) {
//         indexSudoku.addEventListener('mouseover', function() {
//             console.log("Mouseover Sudoku");
//             indexSudoku.classList.add('scaled-sudoku');
//             indexPong.classList.add('shrunken-sudoku');
//         });
        
//         indexSudoku.addEventListener('mouseout', function() {
//             console.log("Mouseout Sudoku");
//             indexSudoku.classList.remove('scaled-sudoku');
//             indexPong.classList.remove('shrunken-sudoku');
//         });
        
//         indexPong.addEventListener('mouseover', function() {
//             console.log("Mouseover Pong");
//             indexPong.classList.add('scaled-pong');
//             indexSudoku.classList.add('shrunken-pong');
//         });
    
//         indexPong.addEventListener('mouseout', function() {
//             console.log("Mouseout Pong");
//             indexPong.classList.remove('scaled-pong');
//             indexSudoku.classList.remove('shrunken-pong');
//         });
//     }
// });



document.addEventListener("DOMContentLoaded", function() {
    console.log("DOMContentLoaded event triggered");
    
    const indexPong = document.querySelector('.index-pong');
    const indexSudoku = document.querySelector('.index-sudoku');
    
    // console.log("indexPong:", indexPong);
    // console.log("indexSudoku:", indexSudoku);
    
    if (indexSudoku && indexPong) {
        // console.log("Event listeners are being attached");
        
        indexSudoku.addEventListener('mouseover', function() {
            console.log("Mouseover Sudoku");
            indexSudoku.classList.add('scaled-sudoku');
            indexPong.classList.add('shrunken-sudoku');
        });
        
        indexSudoku.addEventListener('mouseout', function() {
            console.log("Mouseout Sudoku");
            indexSudoku.classList.remove('scaled-sudoku');
            indexPong.classList.remove('shrunken-sudoku');
        });
        
        indexPong.addEventListener('mouseover', function() {
            console.log("Mouseover Pong");
            indexPong.classList.add('scaled-pong');
            indexSudoku.classList.add('shrunken-pong');
        });
    
        indexPong.addEventListener('mouseout', function() {
            console.log("Mouseout Pong");
            indexPong.classList.remove('scaled-pong');
            indexSudoku.classList.remove('shrunken-pong');
        });
    } else {
        console.log("One or both of the elements not found.");
    }
});

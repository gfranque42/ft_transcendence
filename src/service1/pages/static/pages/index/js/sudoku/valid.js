export function isValidSudoku(board) {
    // Helper function to check if an array has duplicates
    function hasDuplicates(arr) {
        let seen = new Set();
        for (let num of arr) {
            if (num !== '-' && num !== '' && num !== 0 && seen.has(num)) {
                return true;
            }
			if (num !== '-' && num !== '' && num !== 0)
                seen.add(num);
        }
        return false;
    }

    // Check rows
    for (let row of board) {
        if (hasDuplicates(row)) return false;
    }

    // Check columns
    for (let col = 0; col < 9; col++) {
        const column = [];
        for (let row = 0; row < 9; row++) {
            column.push(board[row][col]);
        }
        if (hasDuplicates(column)) return false;
    }

    // Check 3x3 squares
    for (let startRow = 0; startRow < 9; startRow += 3) {
        for (let startCol = 0; startCol < 9; startCol += 3) {
            const square = [];
            for (let row = startRow; row < startRow + 3; row++) {
                for (let col = startCol; col < startCol + 3; col++) {
                    square.push(board[row][col]);
                }
            }
            if (hasDuplicates(square)) return false;
        }
    }

    return true;
}

export function isBoardComplete(board) {
    for (let row of board) {
        if (row.includes('-') || row.includes(' ') || row.includes(0)) return false;
    }
    return true;
}

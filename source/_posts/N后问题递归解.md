title: N后问题递归解
tags:
  - C名题百则
id: 1059
categories:
  - 算法
date: 2015-10-30 15:49:43
---

8后问题(Eight Queen Problem)是指在一个8 * 8的西洋棋盘上要如何放置8个皇后棋且不会互相吃到对方；皇后棋可以吃掉任何它所在的那一列、那一行，以及那两个对角线(米字形)上的任何棋子。请写一个程序，读入一个值n表示棋盘的大小，然后求出n * n格棋盘上放n个皇后棋且不会相互吃掉对方的所有解答。

说明。这是广义的N后问题，因为所要求的是“所有”解答，而不单是其中的一组，对大多数会运用递归的人来说，这个题目反而容易做些。这一类型题目的揭发通常要用到回溯(Backtrack)的技巧--不管用递归还是不用递归都是如此，虽然会浪费时间，但多半会找到答案。

依据题意，写了一个递归的方法，判断是否能放置皇后时有点麻烦，应该有更简便的方法。
``` java
 import java.util.Arrays;

public class NQueens {
	public static int totalNQueens(int n) {
        boolean[][] board = new boolean[n][n];
        return totalNQueens(0, n, board);
    }
	//check if queen can put on board[row][col]
	private static boolean canPutCheck(int row, int col, int n, boolean[][] board) {
		for (int i = 0; i < n; i++) {
			if (board[row][i]) //row
				return false;
			if (board[i][col]) //col
				return false;
		}
		//diagonal
		int i = 0;
		while (row + i < n && col + i < n) {
			if (board[row + i][col +i])
				return false;
			i++;
		}
		i = 0;
		while (row - i >= 0 && col - i >= 0) {
			if (board[row - i][col - i])
				return false;
			i++;
		}
		//back diagonal
		i = 0;
		while (row + i < n && col - i >= 0) {
			if (board[row + i][col - i])
				return false;
			i++;
		}
		i = 0;
		while (row - i >= 0 && col + i < n) {
			if (board[row - i][col + i])
				return false;
			i++;
		}
		return true;

	}
	private static int totalNQueens(int row, int n, boolean[][] board) {
		if (row == n) { 
			return 1;
		}
		int count = 0;
		for (int j = 0; j < n; j++) {
			if (canPutCheck(row, j, n, board)) {
				board[row][j] = true;
				count += totalNQueens(row + 1, n, board);
				board[row][j] = false; //backtrack
			}
		}
		return count;

	}
	public static void main(String[] args) {
		for (int i = 4; i < 10; i++)
			System.out.println(i + " " + totalNQueens(i));
	}
}

```
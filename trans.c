/*
 * trans.c - Matrix transpose B = A^T
 *
 * Each transpose function must have a prototype of the form:
 * void trans(int M, int N, int A[N][M], int B[M][N]);
 *
 * A transpose function is evaluated by counting the number of misses
 * on a 1KB direct mapped cache with a block size of 32 bytes.
 */
#include <stdio.h>
#include "cachelab.h"

int is_transpose(int M, int N, int A[N][M], int B[M][N]);
void trans(int M, int N, int A[N][M], int B[M][N]);
void transpose32x32(int M, int N, int A[N][M], int B[M][N]);
void transpose32x64(int M, int N, int A[N][M], int B[M][N]); 
void transpose64x64(int M, int N, int A[N][M], int B[M][N]); 

/*
 * transpose_submit - This is the solution transpose function that
 *     you will be graded on the assignment. Do not change the
 *     description string "Transpose submission", as the driver
 *     searches for that string to identify the transpose function to
 *     be graded.
 */
char transpose_submit_desc[] = "Transpose submission";
void transpose_submit(int M, int N, int A[N][M], int B[M][N])
{
    if (M==32 && N==32){
      transpose32x32(M, N, A, B);
    }
    else if (M==32 && N==64){
      transpose32x64(M, N, A, B);
    }
    else{
      transpose64x64(M, N, A, B);
    }
}

/*
 * You can define additional transpose functions below. We've defined
 * a simple one below to help you get started.
 */

/*
 * trans - A simple baseline transpose function, not optimized for the cache.
 */
char trans_desc[] = "Simple row-wise scan transpose";
void trans(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, tmp;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; j++) {
            tmp = A[i][j];
            B[j][i] = tmp;
        }
    }

}

void transpose32x32(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, k, c0, c1, c2, c3, c4, c5, c6, c7;
    for (i = 0; i < N; i += 8){
        for (j = 0; j < M; j += 8){
            for (k = i; k < i+8; k++){
                c0 = A[k][j];
                c1 = A[k][j+1];
                c2 = A[k][j+2];
                c3 = A[k][j+3];
                c4 = A[k][j+4];
                c5 = A[k][j+5];
                c6 = A[k][j+6];
                c7 = A[k][j+7];  

                B[j][k] = c0;
                B[j+1][k] = c1;
                B[j+2][k] = c2;
                B[j+3][k] = c3;
                B[j+4][k] = c4;
                B[j+5][k] = c5;
                B[j+6][k] = c6;
                B[j+7][k] = c7;
            }      
        }
    }
}

void transpose32x64(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, k, c0, c1, c2, c3;
    for (i = 0; i < N; i += 8){
        for (j = 0; j < M; j += 4){
            if ((j/4) % 2 == 0){
                for (k = i; k < i+8; k++){
                    c0 = A[k][j];
                    c1 = A[k][j+1];
                    c2 = A[k][j+2];
                    c3 = A[k][j+3];

                    B[j][k] = c0;
                    B[j+1][k] = c1;
                    B[j+2][k] = c2;
                    B[j+3][k] = c3;
                }    
            }    
            else{
                for (k=i+7; k>=i; k--){
                    c0 = A[k][j];
                    c1 = A[k][j+1];
                    c2 = A[k][j+2];
                    c3 = A[k][j+3];

                    B[j][k] = c0;
                    B[j+1][k] = c1;
                    B[j+2][k] = c2;
                    B[j+3][k] = c3;
                }
            }
        }
    }
}

void transpose64x64(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, k, c0, c1, c2, c3, c4, c5, c6, c7;
    for (i = 0; i < N; i += 8){
        for (j = 0; j < M; j += 4){
            if ((j/4) % 2 == 0){
                for (k = i; k < i+8; k++){
                    c0 = A[k][j];
                    c1 = A[k][j+1];
                    c2 = A[k][j+2];
                    c3 = A[k][j+3];
                    
                    if (k==i+1){
                        c4 = A[k][j+4];
                        c5 = A[k][j+5];
                        c6 = A[k][j+6];
                        c7 = A[k][j+7];
                    }

                    B[j][k] = c0;
                    B[j+1][k] = c1;
                    B[j+2][k] = c2;
                    B[j+3][k] = c3;
                }    
            }    
            else{
                for (k=i+7; k>=i; k--){
                    if (k==i+1){
                        B[j][k] = c4;
                        B[j+1][k] = c5;
                        B[j+2][k] = c6;
                        B[j+3][k] = c7;
                    }

                    else{
                        c0 = A[k][j];
                        c1 = A[k][j+1];
                        c2 = A[k][j+2];
                        c3 = A[k][j+3];
                        
                        B[j][k] = c0;
                        B[j+1][k] = c1;
                        B[j+2][k] = c2;
                        B[j+3][k] = c3;
                    }     
                }
            }
        }
    }
}

void test(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, k, c0, c1, c2, c3, c4, c5, c6, c7;
    for (i = 0; i < N; i += 8){
        for (j = 0; j < M; j += 4){
            if ((j/4) % 2 == 0){
                for (k = i; k < i+8; k++){
                        c0 = A[k][j];
                        c1 = A[k][j+1];
                        c2 = A[k][j+2];
                        c3 = A[k][j+3];
                    
                        if (k==i+1){
                            c4 = A[k][j+4];
                            c5 = A[k][j+5];
                            c6 = A[k][j+6];
                            c7 = A[k][j+7];
                        }

                        B[j][k] = c0;
                        B[j+1][k] = c1;
                        B[j+2][k] = c2;
                        B[j+3][k] = c3;
                }    
            }    
            else{
                for (k=i+7; k>=i; k--){
                    if (k==i+1){
                        B[j][k] = c4;
                        B[j+1][k] = c5;
                        B[j+2][k] = c6;
                        B[j+3][k] = c7;
                    }

                    else{
                        c0 = A[k][j];
                        c1 = A[k][j+1];
                        c2 = A[k][j+2];
                        c3 = A[k][j+3];
                        
                        B[j][k] = c0;
                        B[j+1][k] = c1;
                        B[j+2][k] = c2;
                        B[j+3][k] = c3;
                    }     
                }
            }
        }
    }
}

/*
 * registerFunctions - This function registers your transpose
 *     functions with the driver.  At runtime, the driver will
 *     evaluate each of the registered functions and summarize their
 *     performance. This is a handy way to experiment with different
 *     transpose strategies.
 */
void registerFunctions()
{
    /* Register your solution function */
    registerTransFunction(transpose_submit, transpose_submit_desc);

    /* Register any additional transpose functions */
    registerTransFunction(trans, trans_desc);
    registerTransFunction(test, "test");
}

/*
 * is_transpose - This helper function checks if B is the transpose of
 *     A. You can check the correctness of your transpose by calling
 *     it before returning from the transpose function.
 */
int is_transpose(int M, int N, int A[N][M], int B[M][N])
{
    int i, j;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; ++j) {
            if (A[i][j] != B[j][i]) {
                return 0;
            }
        }
    }
    return 1;
}


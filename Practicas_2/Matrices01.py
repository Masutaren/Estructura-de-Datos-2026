
A=[[5,6,13],[5,10,1],[2,11,3]]
B=[[1,2,17],[6,5,15],[3,11,11]]

def MultiMatriz(A,B):
    C=[[0,0,0],[0,0,0],[0,0,0]]
    sum=0
    if len(A[0]) == len(B[0]):
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    sum += A[i][k] * B[k][j]
                C[i][j] = sum
                sum = 0
        print(C)
    else:
        print('La matriz no se puede multiplicar')


MultiMatriz(A,B)

        

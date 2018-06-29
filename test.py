count=0
B=[0]*50
def recursive(A,n):
	global count
	if n==1:
		return 1

	if A[n-1]==0:
		A[n-1]=recursive(A,n-1)
	if A[n-2]==0:
		A[n-2]=recursive(A,n-2)

	A[n]=A[n-1]*A[n-1]+A[n-2]
	B[count]=A[n]
	count+=1
	return A[n]


A=[0]*50
A[0]=0
A[1]=1
A[2]=1


#A[5]=27
x=recursive(A,15)
print(x)
for i in range(len(B)):
	print(B[i])
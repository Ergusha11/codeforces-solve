C++20 (GCC 13-64)

#include <bits/stdc++.h>

#define lp(i,n) for(int i=0;i<n;i++)

using namespace std;

void solution(int n,int k){
	int n1,aux,num;
	aux = INT_MIN;
	num = k;
	while (aux != 0){
		if(num%n==0){
			num++;
			n1 = num/n;
		}
		else{
			n1 = num/n;
		}

		aux = num - n1;
		aux = (k - aux); 
		num = num + aux;
	}
	cout<<num<<endl;
}

int main(){
	int testCases,n,k;
	cin >> testCases;
	lp(i,testCases){
		cin >> n >> k;
		solution(n,k);
	}
	return 0;
}

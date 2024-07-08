C++20 (GCC 13-64)

#include<bits/stdc++.h>
#include <cmath>
#include <vector>

#define lp(i,n) for(int i=0;i<n;i++)

using namespace std;

int pow10(int base){
	int x = 1;
	lp(i,base){
		x *= 10;
	}
	return x;
}

void solution(int num){
	vector<int> numbers;
	int tam,aux,base10,dig;
	tam = 0;
	while(num > 0){
		dig = log10(num);
		base10 = pow10(dig);
		aux = num/base10;
		dig = aux*base10;
		numbers.push_back(dig);
		num = num - dig;
		tam++;
	}

	cout <<tam<<endl;
	lp(i,tam){
		cout<<numbers[i]<<" ";
	}
	cout<<endl;
}

int main(){
	int testCases,num;
	cin >> testCases;
	lp(i,testCases){
		cin >> num;
		solution(num);
	}
}

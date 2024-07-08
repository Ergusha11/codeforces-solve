C++20 (GCC 13-64)

#include<bits/stdc++.h>

using namespace std;

int solution(int num){
	int x;
	x = num/2;
	if(x > 1){
		if((2*x)==num){
			return 1;
		}
	}
	return 0;
}

int main(){
	int num;
	cin >> num;
	if(solution(num)==1){
		cout << "YES"<<endl;
	}
	else{
		cout<<"NO"<<endl;
	}
}



C++20 (GCC 13-64)

#include<bits/stdc++.h>

using namespace std;

int main(){
	int a,b,k,K;
	vector<int> out;
	cin>> a >> b >> k;

	for(int i=1;i<=k;i++){
		K = a*i + b;
		cout<<K <<" ";
	}

	cout<<endl;
}

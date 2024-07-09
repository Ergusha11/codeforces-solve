C++20 (GCC 13-64)

#include<bits/stdc++.h>
#define lp(i,n) for(int i=0;i<n;i++)

using namespace std;

int main (){
	int n,p,num;
	vector<int> numbers;
	cin >> n >> p;
	lp(i,n){
		cin >> num;
		numbers.push_back(num);
	}

	sort(numbers.begin(), numbers.end(), greater<int>());
    
	for (int i = 0; i < n; i++) {
		if(numbers[i]<= p){
			cout << numbers[i] << endl;
			break;
		}
    }

}

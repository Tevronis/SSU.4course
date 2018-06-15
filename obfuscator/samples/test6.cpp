#include <iostream>

using namespace std;

int solve(int n) {
	cout << 2 << endl;
	while (true) {
		for (int i = 0; i < n / 2; i++) {
			cout << i + 1 << endl;
		}
		if (n == 5) {
			break;
		}
	}
	int r;
	r = 90;
	cout << n << endl;

	cout << 3 << endl;
	return 0;
}

int main() {
	cout << 1 << endl;
	int n;
	n = 5;
	for (int i = 0; i < n; i++) {
		cout << i << endl;
	}
	cout << 1.5 << endl;
	n = solve(n);
	cout << "end";
	int x;
	cin >> x;
}
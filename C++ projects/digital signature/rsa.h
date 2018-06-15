#pragma once

#include <iostream> 
#include <math.h> 
#include <vector> 
#include <fstream>
#include <ctime>
#include <string>
#include "BigInt.hpp"

using namespace std;
typedef BigInt BI;
typedef long long ll;

ll gen_long(ll a, ll b) {
	srand(time(0));
	return a + rand() % (b - a);
}

BI gcd(BI a, BI b) {
	return (b != 0) ? gcd(b, a % b) : a;
}

vector <ll> v_prim() {
	vector <ll> prim;
	ifstream p("nastia.txt");
	string num;
	while (getline(p, num))
		prim.push_back(stoll(num));
	return prim;
}


BI gen_e(BI f) {
	BI e;
	for (BI i = 2; i < f; i++)
		if (gcd(i, f) == 1) {
			e = i;
			break;
		}
	return e;
}

ll gcd2(ll a, ll b, ll & x, ll & y) {
	if (a == 0) {
		x = 0;
		y = 1;
		return b;
	}
	ll x1, y1;
	ll d = gcd2(b % a, a, x1, y1);
	x = y1 - (b / a) * x1;
	y = x1;
	return d;
}

BI gen_d(BI f, BI e) {
	ll x, y;
	ll g = gcd2(e.to_long_long(), f.to_long_long(), x, y);
	x = (x%f.to_long_long() + f.to_long_long()) % f.to_long_long();
	//BI d = BI(ans);
	//while ((d*e)%f!="1")
	//	d++;
	//return d;
	return BI(x);
}

pair <pair<BI, BI>, pair<BI, BI>> gen_keys() {
	pair <pair<BI, BI>, pair<BI, BI>> keys;
	vector <ll> prim = v_prim();
	ll p, q;
	p = prim[gen_long(0, prim.size())];
	q = p;
	while (q == p) {
		q = prim[gen_long(0, prim.size())];
	}
	BI N = BI(p)*BI(q);
	BI f = BI(p - 1)*BI(q - 1);
	BI e = gen_e(f);
	BI d = gen_d(f, e);
	keys.first = make_pair(e, N);
	keys.second = make_pair(d, N);

	return keys;
}

int to_int(char a) {
	return int(a);
}


BI powModN(BI x, BI y, BI n) {
	BI result = 1;
	for (BI i = 0; i < y; i++) {
		result = (result * x) % n;
	}
	return result;
}

string crypt(vector <int> text, pair <BI, BI> o_key) {
	string shifr = "";
	BI e = o_key.first;
	BI N = o_key.second;
	ll i = 0;
	while (i < text.size()) {
		string block = "";
		while ((BI(block) * 1000 < N) && (i < text.size())) {
			block += to_string(text[i] + 100);
			i++;
		}
		BI M = BI(block);
		BI c = powm(M, e.to_long_long(), N);
		block = c.to_string();
		block += ' ';
		shifr += block;
	}
	return shifr;
}


vector <int> decrypt(string shifr, pair <BI, BI> s_key) {
	vector <int> text;
	BI d = s_key.first;
	BI N = s_key.second;
	ll i = 0;
	while (i != shifr.size()) {
		string tmp = "";
		while (shifr[i] != ' ') {
			tmp += shifr[i];
			i++;
		}
		BI c = BI(tmp);
		BI M = powm(c, d.to_long_long(), N);
		tmp = M.to_string();
		ll t = 0;
		while (t != tmp.size()) {
			string tmp2 = "";
			for (int j = 0; j < 3; j++) {
				tmp2 += tmp[t];
				t++;
			}
			int ord = stoi(tmp2);
			text.push_back(ord-100);
		}
		i++;
	}
	return text;
}
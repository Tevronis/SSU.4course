#include <iostream>    
#include <fstream>      
#include <vector>
#include <string>
#include "BigInt.hpp"
#include "md5.h"
#include "rsa.h"

using namespace std;

typedef unsigned char byte;

vector<int> read_file(string path) {
	vector<int> result;
	std::ifstream is(path, std::ifstream::binary);
	if (is) {
		// get length of file:
		is.seekg(0, is.end);
		int length = is.tellg();
		is.seekg(0, is.beg);

		char * buffer = new char[length];

		is.read(buffer, length);
		is.close();

		for (int i = 0; i < length; i++) {
			byte b = buffer[i];
			result.push_back(b);
		}

		delete[] buffer;
	}
	return result;
}

void write_file(string path, vector<int> bytes) {
	std::ofstream of(path, std::ifstream::binary);

	char * ww = new char[bytes.size()];

	for (int i = 0; i < bytes.size(); i++)
		ww[i] = byte(bytes[i]);

	of.write(ww, (int)bytes.size());
	delete[] ww;
	of.close();
}

vector<int> string_to_byte(string s) {
	vector<int> result;

	for (int i = 0; i < s.size(); i++) {
		byte b = s[i];
		result.push_back(b);
	}

	return result;
}

int main() {
	setlocale(LC_ALL, "Russian");
	int n;
	cout << "Podpis mod / depodpis mod [1/2]" << endl;
	cin >> n;
	string filename = "7z.exe";
	if (n == 1) {
		MD5 md5;
		string hash = md5.digestFile(&filename[0u]);
		cout << hash << endl;
		cout << "Generation keys" << endl;
		pair <pair<BI, BI>, pair<BI, BI>> keys = gen_keys();
		ofstream out_o("o_key.txt");
		out_o << keys.first.first << ' ' << keys.first.second;
		ofstream out_s("s_key.txt");
		out_s << keys.second.first << ' ' << keys.second.second;

		vector<int> vec = string_to_byte(hash);
		pair <BI, BI> s_key = make_pair(keys.second.first, keys.second.second);
		string shifr = crypt(vec, s_key);
		ofstream out_f("digsig.txt");
		out_f << shifr;
	}
	else {
		MD5 md5;
		string hash = md5.digestFile(&filename[0u]);
		cout << hash << endl;

		string str, tmp;
		string k1 = "", k2 = "";
		ifstream in_key("o_key.txt");
		getline(in_key, tmp);
		int i = 0;
		while (tmp[i] != ' ') {
			k1 += tmp[i];
			i++;
		}
		i++;
		while (tmp[i] != ' ' && i!=tmp.size()) {
			k2 += tmp[i];
			i++;
		}
		pair <BI, BI> o_key = make_pair(BI(k1), BI(k2));

		string rsa_hash;
		ifstream ii("digsig.txt");
		getline(ii, rsa_hash);
	
		vector<int> vec1 = decrypt(rsa_hash, o_key);
		vector<int> vec = string_to_byte(hash);
		if (vec1 == vec)
			cout << "all good!" << endl;
		else {
			cout << "file changed!" << endl;
		}
	}
	return 0;
}
#include <iostream>
#include <string>
#include <vector>
#include <fstream>     
#include <ctime> 
#include "md5.h"

using namespace std;

typedef unsigned char byte;
#define KEY_LEN 10

struct Key {
    vector<int> value;
    vector<string> hashs;
};

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

string vi_to_string(vector<int> &v) {
    string result;

    for (int item: v) {
        result += item + '0';
    }

    return result;
}

vector<Key> gen_keys(int n) {
    vector<Key> result(n);

    int seed = rand() % 1000000;
    cout << "seed: " << seed << endl;
    cout << "Keys:" << endl;
    for (int i = 0; i < n; i++) {
        vector<int> key;
        int remainder = seed;
        for (int j = 0; j < KEY_LEN - 1; j++) {
            int value = rand() % remainder;
            remainder -= value;
            key.push_back(value);
            cout << value << " ";
        }
        cout << remainder << endl;
        key.push_back(remainder);
        result[i].value = key;
    }

    vector<string> hashs;

    cout << "Hashs: " << endl;
    for (Key k: result) {
        MD5 md5;
        string to_hash = vi_to_string(k.value);
		string hash = md5.digestString(&to_hash[0u]);
        hashs.push_back(hash);
        cout << hash << endl;
    }

    for (Key &k: result) {
        k.hashs = hashs;
    }


    return result;
}

vector<int> crypt(vector<int> bytes, Key key) {
    vector<int> result;
    MD5 md5;
    string hashs;
    for (int i = 0; i < key.hashs.size(); i++) {
        hashs += key.hashs[i];
        cout << key.hashs[i] << endl;
    }
	string hash = md5.digestString(&hashs[0u]);
    cout << "masterhash: " << hash << endl;
    int iskey = 0;
    for (int i = 0; i < KEY_LEN; i++) {
        iskey += key.value[i];
    }
    string skey = to_string(iskey);
    cout << "skey: " << skey << endl;
    string master_key = hashs + skey;
    cout << "masterkey: " << master_key << endl;
    cout << "bytessize: " << bytes.size() << endl;
    for (int i = 0; i < bytes.size(); i++) {
        result.push_back(bytes[i] ^ master_key[i % int(master_key.size())]);
    }
    return result;
}

vector<int> decrypt(vector<int> crypted, Key key) {
    vector<int> result;
    MD5 md5;
    string hashs;
    for (int i = 0; i < key.hashs.size(); i++) {
        hashs += key.hashs[i];
    }
	string hash = md5.digestString(&hashs[0u]);

    int iskey = 0;
    for (int i = 0; i < KEY_LEN; i++) {
        iskey += key.value[i];
    }
    string skey = to_string(iskey);
    // start check hashs!
    string hash_skey = md5.digestString(&vi_to_string(key.value)[0u]);
    bool f = false;
    for (string s: key.hashs) 
        if (s == hash_skey)
            f = true;
    
    if (!f) {
        cout << "BAD KEY! ERROR!" << endl;
        exit(0);
    }
    // end check hashs!

    string master_key = hashs + skey;
    for (int i = 0; i < crypted.size(); i++) {
        result.push_back(crypted[i] ^ master_key[i % int(master_key.size())]);
    }
    return result;
}

Key read_key(string keyfile) {
    cout << "read key fun" << endl;
    Key result;
    ifstream in(keyfile);
    for (int i = 0; i < KEY_LEN; i++) {
        int item;
        in >> item;
        result.value.push_back(item);
    }
    cout << "read key fun" << endl;
    while (in.good()) {
        string item;
        in >> item;
        cout << item << endl;
        result.hashs.push_back(item);
    }
    result.hashs.pop_back();
    cout << "read key fun" << endl;
    return result;
}

void write_keys(vector<Key> &keys) {
    for (int i = 0; i < keys.size(); i++) {
            string num = to_string(i);
            std::ofstream of("key_" + num);
            for (int v: keys[i].value)
                of << v << " ";
            for (string h: keys[i].hashs)
                of << h << " ";
        }
}

vector<int> split(string s) {
    vector<int> result;
    string block;
    for (int i = 0; i < s.size(); i++) {
        if (s[i] == ' ') {
            result.push_back(stoi(block));
            block.clear();
            continue;
        }
        block += s[i];
    }
    return result;
}

int main() {
    srand( time( 0 ) );
    int mod;
    cout << "Select mod: keys/crypt/decrypt [1/2/3]";
    cin >> mod;

    string key_f;
    string filename;

    if (mod == 1) {
        cout << "Gen keys mod" << endl;
        vector<Key> keys;
        cout << "Keys count: " << endl;
        int n;
        cin >> n;
        keys = gen_keys(n);
        write_keys(keys);
    }
    if (mod == 2) {
        cout << "Crypt mod" << endl;
        cout << "Select key-file:" << endl;    
        cin >> key_f;
        Key key = read_key(key_f);
        cout << "Select file to crypt:" << endl;
        cin >> filename;
        vector<int> file_b = read_file(filename);
        cout << filename << endl;
        cout << endl;
        vector<int> cryptogram = crypt(file_b, key);
        ofstream cro("en.cr");
        for (int item: cryptogram)  {
            cro << item << " ";
        }
    }
    if (mod == 3) {
        cout << "Decrypt mod" << endl;
        cout << "Select key-file:" << endl;
        cin >> key_f;
        Key key = read_key(key_f);
        cout << "Select file with cryptogram:" << endl;
        cin >> filename;
        ifstream cri(filename);
        string s;
        getline(cri, s);
        vector<int> file_b = split(s);
        vector<int> open_text = decrypt(file_b, key);
        write_file("decrypted.txt", open_text);
    }
}
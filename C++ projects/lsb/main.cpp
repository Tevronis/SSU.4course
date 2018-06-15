#include <iostream>
#include <string>
#include <fstream>      
#include <vector>
#include <bitset>
#include <algorithm>

using namespace std;

typedef unsigned char byte;

string get_bits(unsigned char c) {
    int x = int(c);
    string result;
    for (int i = 0; i < 8; i++) {
        int w = x % 2;
        result += w + '0';
        x /= 2;
    }
    reverse(result.begin(), result.end());
    return result;
}

char get_char(string s) {
    char result;
    int t = 0;
    int tw = 1;
    for (int i = 7; i >= 0; i--) {
        int u = int(s[i]) - 48;
        t += u * tw;
        tw *= 2;
    }
    return char(t);
}

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
	// функция для восстановления файла после дешифровки
	std::ofstream of(path, std::ifstream::binary);

	char * ww = new char[bytes.size()];

	for (int i = 0; i < bytes.size(); i++)
		ww[i] = byte(bytes[i]);

	of.write(ww, (int)bytes.size());
	delete[] ww;
	of.close();
}

void set_data(string text, vector<int> &bin_file) {
    
    string sss;
    for (int i = 0; i < text.size(); i++) {
        string ss = get_bits(text[i]);
        sss += ss;
        //cout << ss << endl;
    }
    
    int adress_pixel = bin_file[10];
    //cout << adress_pixel << endl; 255 11111111
    int j = 0;
    for (int i = adress_pixel; i < bin_file.size() && j < sss.size(); i+=3, j++) {
        if (sss[j] == '1') {
            if (bin_file[i] % 2 == 0) {
                bin_file[i]++;
            }   
        } else {
            if (bin_file[i] % 2 == 1) {
                bin_file[i]--;
            }
        }
    }
}

string get_data(vector<int> bin_file) {
    cout << "start get_data" << endl;
    
    string result;
    
    int adress_pixel = bin_file[10];
    //cout << adress_pixel << endl;
    string block;
    for (int i = adress_pixel; i < bin_file.size(); i+=3) {
        int bit = bin_file[i] % 2;
        block += char(bit + 48);
        if (block.size() == 8) {
            char c = get_char(block);
            result += c;
            block.clear();
        }
    }
    return result;
}

int main() {
    int mod;
    string filename;
    cout << "Write or read data [1/2]" << endl;
    cin >> mod;

    if (mod == 1) {
        cout << "What is file?" << endl;
        cin >> filename;
        vector<int> vec = read_file(filename);
        string text;
        cout << "please write text to set: " << endl;
        cin >> text;
        set_data(text, vec);
        write_file("withmsg.bmp", vec);
    } else {
        vector<int> vec = read_file("withmsg.bmp");
        string text = get_data(vec);
        std::ofstream of("text.txt");
        of << text;
    }
}
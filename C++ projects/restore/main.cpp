#include <windows.h>
#include <iostream>
#include <tlhelp32.h>
#include <string>
#include <fstream>


using namespace std;

bool IsProcessRun( const char * const processName )
{
   HANDLE hSnapshot = CreateToolhelp32Snapshot( TH32CS_SNAPPROCESS, 0 );

   PROCESSENTRY32 pe;
   pe.dwSize = sizeof( PROCESSENTRY32 );
   Process32First( hSnapshot, &pe );

   while( 1 ) {
        if( strcmp( pe.szExeFile, processName ) == 0 ) 
                return true;
        if( !Process32Next( hSnapshot, &pe ) ) 
                return false;
   }
}

bool FileExists(char *fname) {
	bool isExist = false;
	std::ifstream fin(fname);
	
	if(fin.is_open())
		isExist = true;
	
	fin.close();
	return isExist;
}

void restore(char * FILE, string current_filename) {
	if (!FileExists(FILE)) {
		cout << FILE << " not exist! Try to restore this!" << endl;
		ifstream infile(current_filename.c_str(), ios::binary);
		ofstream outfile(FILE, ios::binary);
		outfile << infile.rdbuf();
		cout << "Restore success!" << endl;
	}
	if (!IsProcessRun(FILE)) {
        cout << FILE << " not run! Try to run procces!" << endl;
		ShellExecute ( NULL, NULL, FILE,NULL, NULL, SW_SHOWNORMAL );
	}
}

bool sleep_time() {
	/*for (int i = 0; i < 1000000000; i++) {
	}*/
	Sleep(5000);
	return true;
}

int main(int argc, char **argv) {

	std::string s_path(*argv);
	std::string filename = s_path.substr(s_path.find_last_of("\\") + 1);
	cout << "Current file: " << filename << endl;
	while (sleep_time()) {
		if (filename == "prog1.exe") {
			char FILE[] = "prog2.exe";
			restore(FILE, filename);
		} else {
			char FILE[] = "prog1.exe";
			restore(FILE, filename);
		}
	}

 	return 0;
}
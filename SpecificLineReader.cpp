#include <fstream>
#include <limits>
#include <iostream>

std::fstream& GotoLine(std::fstream& file, unsigned int num){
    file.seekg(std::ios::beg);
    for(int i=0; i < num - 1; ++i){
        file.ignore(std::numeric_limits<std::streamsize>::max(),'\n');
    }
    return file;
}

/*
std::string getLineStr(int line)
{
    using namespace std;
    fstream file("69M_reddit_accounts.csv");

    GotoLine(file, 69382538);

    string line8;
    file >> line8;

    return line8;
}
*/

int main(int argc, char *argv[])
{
    using namespace std;
    fstream file("69M_reddit_accounts.csv");

    int line_num;

    line_num >> atoi(argv[1]);

    cout << line_num;

    GotoLine(file, line_num);

    string line8;
    file >> line8;

    cout << line8 << endl;

    return 0;
}

/*
extern "C"{
    std::string getLineString(int line){
        return getLineStr(line);
    }
}
*/
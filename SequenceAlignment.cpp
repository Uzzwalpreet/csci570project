#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ifstream file("/Users/uzzwalpreetkaur/Desktop/Project-2/SampleTestCases/input1.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return 1;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }

    file.close();
    return 0;
}

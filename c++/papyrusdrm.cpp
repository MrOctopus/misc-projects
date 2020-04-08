#include <iostream>
#include <fstream>
#include <random>

const std::uint32_t MAGIC_NUMBER = 0xFA57C0DE;

int main(int argc, char* argv[])
{
    if (argc < 2) { std::cout << "ERR 1: No file given"; return 1; }
    
    std::fstream file(argv[1], std::fstream::in | std::fstream::out | std::ifstream::binary);

    if (file.bad()) { std::cout << "ERR 2: Bad file"; return 2; }

    std::uint32_t fileStream = 0;
    std::uint8_t* fileStreamBytes = reinterpret_cast<std::uint8_t*>(&fileStream);

    file.read(reinterpret_cast<char*>(&fileStream), sizeof(fileStream));

    if (file.gcount() != sizeof(fileStream)) { std::cout << "ERR 3: Couldn't read file"; return 3; }

    std::swap(fileStreamBytes[0], fileStreamBytes[3]);
    std::swap(fileStreamBytes[1], fileStreamBytes[2]);

    if (fileStream != MAGIC_NUMBER) { std::cout << "ERR 4: Magic number doesn't match"; return 4; }

    file.seekg(sizeof(uint32_t), std::ios_base::cur);
    file.read(reinterpret_cast<char*>(&fileStream), sizeof(fileStream));

    if (fileStream != 0) { std::cout << "ERR 5: File has already been locked"; return 5; }

    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_int_distribution<uint32_t> dist(UINT8_MAX + 1, UINT32_MAX);
    fileStream = dist(mt);

    file.seekp(sizeof(uint64_t), std::ios_base::beg);
    file.write(reinterpret_cast<char*>(&fileStream), sizeof(fileStream));
    fileStream = dist(mt);
    file.write(reinterpret_cast<char*>(&fileStream), sizeof(fileStream));

    std::cout << "SUCCESS! File locked";
    return 0;
}
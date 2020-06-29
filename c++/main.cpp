#include <iostream>

#include "Mapa.hpp"

int main() {
    std::cout << "Bem vindo ao programa da formiga!" << std::endl;
    Mapa m{10, 10};
    m.mapaRandom(0.80);
    m.showMapa();
    
    return 0;
}
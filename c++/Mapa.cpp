#include <iostream>
#include <stdlib.h>
#include <time.h>
#include "Mapa.hpp"

Mapa::Mapa(const unsigned short x, const unsigned short y):x{x},y{y}{
    mapa.resize(x, std::vector<bool>(y, false));
}
Mapa::~Mapa(){}

void Mapa::mapaRandom(const float porcentagem) {
    unsigned short x, y;
    srand(time(NULL));
    short total = this->x * this->y * porcentagem;
    for(int i = 0; i < total; ++i){
        x = rand()%this->x;
        y = rand()%this->y;
        while(mapa[x][y]){
            x = rand()%this->x;
            y = rand()%this->y;
        }
        mapa[x][y] = true;
    }
}

void Mapa::showMapa() const {
    for(int i = 0; i < this->x; ++i){
        for(int j = 0; j < this->y; ++j)
            std::cout << mapa[i][j] << " ";
        std::cout << std::endl;
    }
}   
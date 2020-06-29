#ifndef MAPA_HPP
#define MAPA_HPP

#include <vector>

class Mapa{
    public:
        Mapa(const unsigned short x, const unsigned short y);
        ~Mapa();
        void mapaRandom(const float porcentagem);
        void showMapa() const;
    private:
        unsigned short x, y;
        std::vector<std::vector<bool>> mapa;
};

#endif
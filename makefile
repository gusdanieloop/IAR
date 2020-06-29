parametrosCompilacao=-Wall -O3
nomeAula=formigas

all: $(nomeAula)

$(nomeAula): main.o Mapa.o 
	g++ -o $(nomeAula) main.o Mapa.o $(parametrosCompilacao)

main.o: main.cpp
	g++ -c main.cpp $(parametrosCompilacao)

Mapa.o: Mapa.hpp Mapa.cpp
	g++ -c Mapa.cpp $(parametrosCompilacao)

clean:
	rm -f *.o *.gch $(nomeAula)
CXX = clang++
CXXFLAGS = -std=c++20 -O2 -Wall

DAYS = $(patsubst src/%.cpp,%,$(wildcard src/*.cpp))

all: $(DAYS)

%: src/%.cpp | build
	$(CXX) $(CXXFLAGS) $< -o build/$@

build:
	mkdir -p build

clean:
	rm -rf build

.PHONY: all clean

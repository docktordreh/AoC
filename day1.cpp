#include <algorithm>
#include <bits/stdc++.h>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
struct elve {
  int id;
  int calories;
  elve(int id) : id(id) {}
};
bool operator<(elve e1, elve e2) { return e1.calories < e2.calories; }

int main() {
  std::ifstream in;
  in.open("day1.txt");
  std::vector<int> vec;
  vec.push_back(0);
  int counter = 0;
  std::string s;
  while (in) {
    std::getline(in, s);
    if (s.length() == 0) {
      ++counter;
      vec.push_back(0);
      continue;
    }
    int cal = stoi(s);
    vec[counter] += cal;
  }
  std::make_heap(vec.begin(), vec.end());
  int max = vec.front();
  std::pop_heap(vec.begin(), vec.end());
  vec.pop_back();
  max += vec.front();
  std::pop_heap(vec.begin(), vec.end());
  vec.pop_back();
  max += vec.front();
  std::pop_heap(vec.begin(), vec.end());
  vec.pop_back();

  std::cout << "max is " << max << std::endl;
  return 0;
}

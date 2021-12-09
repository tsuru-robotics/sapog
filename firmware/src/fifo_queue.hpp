/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <array>
#include <cassert>

namespace silver_template_library
{
// wrapper around an array to make it a fifo queue
template<typename T, int size>
class Queue
{
public:
  std::array<T, size> array;
  std::size_t counter;

  T pop();

  void push(T element);
};

template<typename T, int size>
T Queue<T, size>::pop()
{
  return this->array.at(counter--);
}

template<typename T, int size>
void Queue<T, size>::push(T element)
{
  if (++counter > size)
  {
    counter = 0;
    assert(false);
  }
  this->array.at(counter) = element;
}

}

/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <array>
#include <cassert>
#include "zubax_chibios/sys/sys.hpp"

namespace silver_template_library
{
// wrapper around an array to make it a fifo queue
template<typename T, int size>
class Queue
{
public:
  std::array<T, size> array;
  int counter;

  T pop();

  void push(T element);
};

template<typename T, int size>
T Queue<T, size>::pop()
{
  os::CriticalSectionLocker lock;
  if (counter == -1)
  {
    assert(false);
  }
  return this->array.at(counter--);
}

template<typename T, int size>
void Queue<T, size>::push(T element)
{
  os::CriticalSectionLocker lock;
  if (++counter > size)
  {
    counter = 0;
    assert(false);
  }
  this->array.at(counter) = element;
}

}

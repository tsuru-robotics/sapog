/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <array>
#include <cassert>
#include <cstdio>
#include <optional>
#include "zubax_chibios/sys/sys.hpp"

namespace silver_template_library
{
// wrapper around an array to make it a fifo queue
template<typename T, int size>
class Queue
{
public:
  std::array<T, size> array;
  int counter = 0;

  std::optional<T> pop();

  void push(T element);
};

template<typename T, int size>
std::optional<T> Queue<T, size>::pop()
{
  if (counter == -1)
  {
    return {};
  }
  return this->array.at(counter--);
}

template<typename T, int size>
void Queue<T, size>::push(T element)
{
  if (++counter >= size)
  {
    //printf("Fifo queue filled up!\n");
    counter = 0;
    assert(false);
  }
  this->array.at(counter) = element;
}

}

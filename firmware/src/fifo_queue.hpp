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
template<typename T, int capacity>
class Queue
{
public:
  std::array<T, capacity> array;
  int push_counter = 0;
  int pop_counter = 0;
  int length = 0;

  std::optional<T> pop();

  void push(T const &element);

  void reset();
};

template<typename T, int capacity>
std::optional<T> Queue<T, capacity>::pop()
{
  if (length > 0)
  {
    auto &return_value = this->array.at(pop_counter);
    pop_counter++;
    if (pop_counter >= capacity)
    {
      pop_counter = 0;
    }
    length--;
    return return_value;
  } else
  {
    return {};
  }
}

template<typename T, int capacity>
void Queue<T, capacity>::push(T const &element)
{
  this->array.at(push_counter) = element;
  if (++push_counter >= capacity)
  {
    //printf("Fifo queue filled up!\n");
    push_counter = 0;
  }
  length++;
  if (length > capacity)
  {
    // Then we basically pop one element to make room for the new one.
    // This happens say when one of the can cables gets destroyed and replaced in flight
    // then the connection that was resurrected will have a full queue
    length = capacity; // like length--;
    pop_counter++;
    if (pop_counter >= capacity)
    {
      pop_counter = 0;
    }
  }
}

template<typename T, int capacity>
void Queue<T, capacity>::reset()
{
  push_counter = 0;
  pop_counter = 0;
  length = 0;
}
}

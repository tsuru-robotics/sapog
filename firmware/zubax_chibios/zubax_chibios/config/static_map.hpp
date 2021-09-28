#ifndef FIRMWARE_STATIC_MAP_HPP
#define FIRMWARE_STATIC_MAP_HPP
#include <optional>
namespace mtl
{
template<typename Tkey, typename Tvalue, size_t max_size>
class StaticMap
{
public:
    const size_t size = max_size;
    Tkey key_array[max_size];
    Tvalue value_array[max_size];
    std::optional<Tvalue> getValue(Tkey key);

    bool setValue(Tkey key, Tvalue value);

    int getIndexFromName(Tkey name);
};
}

#endif //FIRMWARE_STATIC_MAP_HPP

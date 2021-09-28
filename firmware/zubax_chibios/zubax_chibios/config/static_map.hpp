#ifndef FIRMWARE_STATIC_MAP_HPP
#define FIRMWARE_STATIC_MAP_HPP
namespace std
{
template<typename Tkey, typename Tvalue, size_t max_size>
class StaticMap
{
private:
    constexpr static size_t size = max_size;
    Tkey key_array[max_size];
    Tvalue value_array[max_size];
public:
    Tvalue getValue(Tkey key);

    bool setValue(Tkey key, Tvalue value);

    int getIndexFromName(Tkey name);
};
}

#endif //FIRMWARE_STATIC_MAP_HPP

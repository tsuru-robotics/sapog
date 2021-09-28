#include "static_map.hpp"


namespace std
{
template<typename Tkey, typename Tvalue, size_t max_size>
std::optional<Value> StaticMap<Tkey, Tvalue>::getValue(Tkey key)
{
    if(int i = getIndexFromName(key); i >= 0){
        return value_array[i];
    }
    return {};
}

template<typename Tkey, typename Tvalue, size_t max_size>
bool StaticMap<Tkey, Tvalue>::setValue(Tkey key, Tvalue value)
{

}

template<typename Tkey, typename Tvalue, size_t max_size>
int StaticMap<Tkey, Tvalue, max_size>::getIndexFromName(Tkey& name)
{
    for (int i = 0; i < max_size; ++i)
    {
        if (key_array[i] == name)
        {
            return i;
        }
    }
    return -1;
}
}
